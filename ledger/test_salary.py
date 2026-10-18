from datetime import date
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from .models import Activity, Account, Entry, Salary, SalaryReceipt
from .services import save_entry, void_entry, summary
from .salary_services import save_salary, link_receipt, unlink_receipt, salary_totals


@override_settings(ALLOWED_HOSTS=["testserver"])
class SalaryTests(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user("ensayo_sueldo", password="Ensayo!527-local")
        self.activity=Activity.objects.create(owner=self.user,name="Personal")
        self.account=Account.objects.create(owner=self.user,name="Cuenta",kind="banco")

    def salary(self, **changes):
        values=dict(owner=self.user,title="Sueldo de ensayo",activity=self.activity,mode="neto",net_cents=100000,earned_month=date(2026,8,1),budget_month=date(2026,9,1),expected_date=date(2026,9,5))
        return save_salary(Salary(**{**values,**changes}),self.user)

    def income(self,cents=40000,**changes):
        values=dict(owner=self.user,kind="ingreso",cents=cents,activity=self.activity,account=self.account,date=date(2026,10,2),description="Cobro sintético")
        return save_entry(Entry(**{**values,**changes}),self.user)

    def test_forecast_and_partial_receipts_do_not_duplicate_cash(self):
        salary=self.salary()
        self.assertEqual(summary(self.user)["balance"],0)
        for amount in (40000,30000): link_receipt(salary,self.income(amount),self.user)
        row=salary_totals(self.user,date(2026,9,1))
        self.assertEqual((row["planned"],row["received"],row["pending"]),(100000,70000,30000))
        self.assertEqual(summary(self.user)["income"],70000)
        self.assertEqual(Entry.objects.count(),2)
        self.assertEqual(salary_totals(self.user,date(2026,10,1))["received"],0)

    def test_details_and_months_are_validated(self):
        self.salary(mode="detalle",gross_cents=120000,additions_cents=5000,deductions_cents=25000)
        for changes in ({"earned_month":date(2026,8,2)},{"net_cents":0},{"mode":"detalle","gross_cents":120000,"net_cents":90000}):
            with self.subTest(changes=changes),self.assertRaises(ValidationError): self.salary(**changes)

    def test_no_duplicate_or_foreign_receipts(self):
        salary=self.salary()
        entry=self.income()
        link_receipt(salary,entry,self.user)
        with self.assertRaises(ValidationError): link_receipt(self.salary(),entry,self.user)
        other=get_user_model().objects.create_user("otro_sueldo")
        other_activity=Activity.objects.create(owner=other,name="Privada")
        with self.assertRaises(ValidationError): self.salary(activity=other_activity)
        with self.assertRaises(ValidationError): link_receipt(salary,self.income(kind="gasto"),self.user)

    def test_entry_corrections_and_void_affect_receipts_without_duplication(self):
        salary=self.salary()
        entry=self.income()
        link_receipt(salary,entry,self.user)
        entry.cents=60000
        save_entry(entry,self.user,1,"Corregir cobro")
        self.assertEqual(salary_totals(self.user,date(2026,9,1))["received"],60000)
        entry.kind="gasto"
        with self.assertRaises(ValidationError): save_entry(entry,self.user,2,"Cambio incompatible")
        entry.refresh_from_db()
        void_entry(entry,self.user,2,"Anular ensayo")
        self.assertEqual(salary_totals(self.user,date(2026,9,1))["received"],0)
        self.assertEqual(SalaryReceipt.objects.count(),1)

    def test_salary_revision_and_unlink_preserve_income(self):
        salary=self.salary()
        receipt=link_receipt(salary,self.income(),self.user)
        salary.title="Título corregido"
        save_salary(salary,self.user,1,"Ajustar título")
        with self.assertRaises(ValidationError): save_salary(salary,self.user,1,"Edición obsoleta")
        with self.assertRaises(ValidationError): unlink_receipt(receipt,self.user,"")
        unlink_receipt(receipt,self.user,"Clasificación incorrecta")
        self.assertEqual(summary(self.user)["balance"],40000)
        self.assertEqual(salary_totals(self.user,date(2026,9,1))["pending"],100000)

    def test_access_and_salary_forms(self):
        self.assertEqual(self.client.get("/app/sueldo/").status_code,302)
        self.client.force_login(self.user)
        self.assertContains(self.client.get("/app/sueldo/"),"Mi sueldo")
        response=self.client.get("/app/sueldo/nuevo/")
        form=response.context["form"]
        data={"title":"Plan sintético","activity":str(self.activity.pk),"mode":"detalle","earned_month":"2026-08","budget_month":"2026-09","expected_date":"2026-09-05","gross_amount":"1200","additions_amount":"50","deductions_amount":"250","version":"0","submission":str(form.initial["submission"]),"active":"on"}
        self.assertEqual(self.client.post("/app/sueldo/nuevo/",data).status_code,302)
        self.assertEqual(self.client.post("/app/sueldo/nuevo/",data).status_code,400)
        self.assertEqual(Salary.objects.get().net_cents,100000)
        self.assertEqual(Entry.objects.count(),0)

    def test_backups_include_salary_and_keep_legacy_compatibility(self):
        import json,hashlib,tempfile
        from .backups import export_backup,restore_backup,canonical
        salary=self.salary()
        link_receipt(salary,self.income(),self.user)
        raw=export_backup(self.user)
        with tempfile.TemporaryDirectory() as folder,override_settings(BACKUP_DIR=folder):
            restore_backup(self.user,raw)
            self.assertEqual(salary_totals(self.user,date(2026,9,1))["received"],40000)
            legacy=json.loads(raw)
            legacy["format"]=1
            for key in ("salaries","salary_receipts"): legacy["objects"].pop(key)
            legacy.pop("sha256")
            legacy["sha256"]=hashlib.sha256(canonical(legacy)).hexdigest()
            restore_backup(self.user,canonical(legacy))
        self.assertEqual(Salary.objects.count(),0)
        self.assertEqual(SalaryReceipt.objects.count(),0)
        self.assertEqual(summary(self.user)["income"],40000)

    def test_invalid_salary_backup_rolls_back(self):
        import json,hashlib,tempfile
        from .backups import export_backup,restore_backup,canonical
        salary=self.salary()
        link_receipt(salary,self.income(),self.user)
        for field,value in (("earned_month","fecha-no-valida"),("activity_id","00000000-0000-0000-0000-000000000001"),("revision",0)):
            payload=json.loads(export_backup(self.user))
            payload["objects"]["salaries"][0]["fields"][field]=value
            payload.pop("sha256")
            payload["sha256"]=hashlib.sha256(canonical(payload)).hexdigest()
            with self.subTest(field=field),tempfile.TemporaryDirectory() as folder,override_settings(BACKUP_DIR=folder),self.assertRaises(ValidationError):
                restore_backup(self.user,canonical(payload))
            self.assertEqual(SalaryReceipt.objects.count(),1)
            self.assertEqual(salary_totals(self.user,date(2026,9,1))["received"],40000)

    def test_receipt_views_preserve_income_and_permissions(self):
        from django.test import Client
        salary=self.salary()
        entry=self.income()
        self.client.force_login(self.user)
        self.assertEqual(self.client.post(f"/app/sueldo/{salary.pk}/cobro/",{"entry":str(entry.pk)}).status_code,302)
        receipt=SalaryReceipt.objects.get()
        self.assertEqual(self.client.get(f"/app/sueldo/cobro/{receipt.pk}/desvincular/").status_code,200)
        self.assertEqual(self.client.post(f"/app/sueldo/cobro/{receipt.pk}/desvincular/",{"reason":"Ensayo","confirm":"on"}).status_code,302)
        self.assertEqual(Entry.objects.count(),1)
        self.assertEqual(summary(self.user)["income"],40000)
        protected=Client(enforce_csrf_checks=True)
        protected.force_login(self.user)
        self.assertEqual(protected.post("/app/sueldo/nuevo/",{}).status_code,403)
        other=get_user_model().objects.create_user("intruso")
        self.client.force_login(other)
        self.assertEqual(self.client.get(f"/app/sueldo/{salary.pk}/").status_code,404)
        self.assertEqual(self.client.get(f"/app/sueldo/{salary.pk}/cobro/").status_code,404)

    def test_activity_changes_and_inactive_forecasts(self):
        salary=self.salary()
        link_receipt(salary,self.income(120000),self.user)
        row=salary_totals(self.user,date(2026,9,1))["rows"][0]
        self.assertEqual((row["pending"],row["excess"]),(0,20000))
        salary.activity=Activity.objects.create(owner=self.user,name="Otro ámbito")
        with self.assertRaises(ValidationError): save_salary(salary,self.user,1,"Cambiar actividad")
        salary.refresh_from_db()
        salary.active=False
        save_salary(salary,self.user,1,"Excluir previsión")
        total=salary_totals(self.user,date(2026,9,1))
        self.assertEqual((total["planned"],total["pending"],total["received"]),(0,0,120000))
