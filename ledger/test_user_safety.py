import json
import tempfile
from datetime import date
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.core.management import call_command, CommandError
from .models import Activity, Account, Entry, Salary, SalaryReceipt, AuditEvent, Installation
from .services import save_entry, summary
from .salary_services import save_salary, link_receipt
from .backups import restore_backup

@override_settings(ALLOWED_HOSTS=["testserver"])
class UserSafetyTests(TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.override=override_settings(BACKUP_DIR=self.folder.name)
        self.override.enable()
        self.addCleanup(self.override.disable)
        User=get_user_model()
        self.admin=User.objects.create_user("admin_ensayo",password="Ensayo-local!837",is_staff=True)
        self.user=User.objects.create_user("usuario_ensayo",password="Ensayo-local!837")
        Installation.objects.create(user=self.admin)
        self.activity=Activity.objects.create(owner=self.user,name="Personal")
        self.account=Account.objects.create(owner=self.user,name="Banco",kind="banco")
        self.entry=save_entry(Entry(owner=self.user,date=date(2026,9,1),kind="ingreso",description="Ingreso sintético",cents=10000,activity=self.activity,account=self.account),self.user)
        self.client.force_login(self.user)

    def confirmation(self,word="ELIMINAR",**changes):
        return {"current_password":"Ensayo-local!837","phrase":word,"reason":"Revisión de ensayo","confirm":"on","version":"1",**changes}

    def test_roles_and_profile_cannot_escalate(self):
        self.assertEqual(self.client.get("/app/usuarios/").status_code,403)
        self.assertEqual(self.client.post("/app/usuarios/nuevo/",{}).status_code,403)
        response=self.client.post("/app/perfil/editar/",{"username":self.user.username,"first_name":"Nombre de ensayo","last_name":"","current_password":"Ensayo-local!837","is_staff":"on"})
        self.assertEqual(response.status_code,302)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.user.first_name,"Nombre de ensayo")
        self.assertContains(self.client.get("/app/perfil/"),"Nombre de ensayo")
        self.assertContains(self.client.get("/app/resumen/"),"Menú de usuario")

    def test_admin_creates_normal_user_and_cannot_disable_self(self):
        self.client.force_login(self.admin)
        response=self.client.post("/app/usuarios/nuevo/",{"username":"nueva_persona","first_name":"Ensayo","last_name":"","password1":"Persona-ensayo!537","password2":"Persona-ensayo!537","role":"normal","current_password":"Ensayo-local!837"})
        self.assertEqual(response.status_code,302)
        person=get_user_model().objects.get(username="nueva_persona")
        self.assertFalse(person.is_staff)
        self.assertEqual(Activity.objects.filter(owner=person).count(),1)
        self.assertFalse(Entry.objects.filter(owner=person).exists())
        response=self.client.post(f"/app/usuarios/{self.admin.pk}/",{"role":"normal","current_password":"Ensayo-local!837","confirm":"on"})
        self.assertEqual(response.status_code,400)
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active and self.admin.is_staff)
        self.assertEqual(self.client.get(f"/app/eliminar/movimiento/{self.entry.pk}/").status_code,404)

    def test_deletion_requires_post_password_phrase_and_own_record(self):
        url=f"/app/eliminar/movimiento/{self.entry.pk}/"
        self.assertEqual(self.client.get(url).status_code,200)
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk).exists())
        for changes in ({"current_password":"mal"},{"phrase":"mal"},{"confirm":""},{"version":"0"}):
            self.assertEqual(self.client.post(url,self.confirmation(**changes)).status_code,400)
        self.assertEqual(self.client.post(url,self.confirmation()).status_code,302)
        self.assertFalse(Entry.objects.filter(pk=self.entry.pk).exists())
        self.assertEqual(summary(self.user)["balance"],0)
        self.assertTrue(AuditEvent.objects.filter(owner=self.user,action="eliminación").exists())

    def test_backup_failure_and_references_do_not_delete(self):
        url=f"/app/eliminar/movimiento/{self.entry.pk}/"
        with patch("ledger.safety_services.write_backup",side_effect=OSError("ensayo")):
            self.assertEqual(self.client.post(url,self.confirmation()).status_code,400)
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk).exists())
        self.assertEqual(self.client.post(f"/app/eliminar/cuenta/{self.account.pk}/",self.confirmation()).status_code,400)
        self.assertTrue(Account.objects.filter(pk=self.account.pk).exists())

    def salary(self):
        return save_salary(Salary(owner=self.user,title="Plan",activity=self.activity,mode="neto",earned_month=date(2026,8,1),budget_month=date(2026,9,1),expected_date=date(2026,9,1),net_cents=10000),self.user)

    def test_salary_delete_preserves_income_and_entry_delete_unlinks(self):
        salary=self.salary()
        link_receipt(salary,self.entry,self.user)
        self.assertEqual(self.client.post(f"/app/eliminar/sueldo/{salary.pk}/",self.confirmation()).status_code,302)
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk).exists())
        self.assertFalse(SalaryReceipt.objects.exists())
        salary=self.salary()
        link_receipt(salary,self.entry,self.user)
        self.assertEqual(self.client.post(f"/app/eliminar/movimiento/{self.entry.pk}/",self.confirmation()).status_code,302)
        self.assertTrue(Salary.objects.filter(pk=salary.pk).exists())
        self.assertFalse(SalaryReceipt.objects.exists())

    def test_reset_only_own_finances_preserves_access_and_can_restore(self):
        other=Activity.objects.create(owner=self.admin,name="Ajena")
        other_account=Account.objects.create(owner=self.admin,name="Ajena",kind="banco")
        other_entry=save_entry(Entry(owner=self.admin,date=date(2026,9,1),kind="ingreso",description="Privado de otra persona",cents=7777,activity=other,account=other_account),self.admin)
        other_salary=save_salary(Salary(owner=self.admin,title="Plan ajeno",activity=other,mode="neto",earned_month=date(2026,8,1),budget_month=date(2026,9,1),expected_date=date(2026,9,1),net_cents=7777),self.admin)
        other_receipt=link_receipt(other_salary,other_entry,self.admin)
        self.assertEqual(self.client.get("/app/reiniciar/").status_code,200)
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk).exists())
        password=self.user.password
        response=self.client.post("/app/reiniciar/",self.confirmation("REINICIAR usuario_ensayo",owner=str(self.admin.pk)))
        self.assertEqual(response.status_code,302)
        self.assertTrue(Activity.objects.filter(pk=other.pk).exists())
        self.assertTrue(Account.objects.filter(pk=other_account.pk).exists())
        self.assertTrue(Entry.objects.filter(pk=other_entry.pk).exists())
        self.assertTrue(Salary.objects.filter(pk=other_salary.pk).exists())
        self.assertTrue(SalaryReceipt.objects.filter(pk=other_receipt.pk).exists())
        self.assertEqual(summary(self.admin)["balance"],7777)
        self.assertFalse(Entry.objects.filter(owner=self.user).exists())
        self.assertEqual(Activity.objects.filter(owner=self.user).count(),1)
        self.user.refresh_from_db()
        self.assertEqual(self.user.password,password)
        from pathlib import Path
        raw=list(Path(self.folder.name).glob(f"usuario-{self.user.pk}/*.json"))[0].read_bytes()
        self.assertNotIn(b"Privado de otra persona",raw)
        restore_backup(self.user,raw)
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk).exists())
        self.assertTrue(Activity.objects.filter(pk=other.pk).exists())

    def test_csrf_and_deactivation_and_cli_target(self):
        csrf=Client(enforce_csrf_checks=True)
        csrf.force_login(self.user)
        self.assertEqual(csrf.post("/app/reiniciar/",self.confirmation("REINICIAR usuario_ensayo")).status_code,403)
        with self.assertRaises(CommandError): call_command("respaldo_finanzas")
        self.client.force_login(self.admin)
        response=self.client.post(f"/app/usuarios/{self.user.pk}/",{"role":"normal","current_password":"Ensayo-local!837","confirm":"on"})
        self.assertEqual(response.status_code,302)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get("/app/resumen/").status_code,302)

    def test_password_change_keeps_current_session_and_invalidates_other(self):
        other=Client()
        other.force_login(self.user)
        response=self.client.post("/clave/",{"old_password":"Ensayo-local!837","new_password1":"Clave-nueva!783-ensayo","new_password2":"Clave-nueva!783-ensayo"})
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.client.get("/app/resumen/").status_code,200)
        self.assertEqual(other.get("/app/resumen/").status_code,302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Clave-nueva!783-ensayo"))

    def test_reset_rejects_wrong_confirmation_and_catalog_can_delete_unused(self):
        self.assertEqual(self.client.post("/app/reiniciar/",self.confirmation("REINICIAR otro_usuario")).status_code,400)
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk).exists())
        with patch("ledger.safety_services.write_backup",side_effect=OSError("ensayo")):
            self.assertEqual(self.client.post("/app/reiniciar/",self.confirmation("REINICIAR usuario_ensayo")).status_code,400)
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk).exists())
        empty=Account.objects.create(owner=self.user,name="Vacía",kind="efectivo")
        self.assertEqual(self.client.post(f"/app/eliminar/cuenta/{empty.pk}/",self.confirmation()).status_code,302)
        self.assertFalse(Account.objects.filter(pk=empty.pk).exists())
        foreign=Account.objects.create(owner=self.admin,name="Privada",kind="banco")
        self.assertEqual(self.client.post(f"/app/eliminar/cuenta/{foreign.pk}/",self.confirmation()).status_code,404)
        self.assertTrue(Account.objects.filter(pk=foreign.pk).exists())

    def test_cli_requires_explicit_owner_and_restore_keeps_others(self):
        from io import StringIO
        from pathlib import Path
        output=StringIO()
        call_command("respaldo_finanzas",usuario=self.user.username,stdout=output)
        path=Path(output.getvalue().strip())
        self.assertIn(f"usuario-{self.user.pk}",str(path))
        with self.assertRaises(CommandError):
            call_command("restaurar_finanzas",str(path),confirmar=True)
        before=self.admin.password
        call_command("restaurar_finanzas",str(path),usuario=self.user.username,confirmar=True,stdout=StringIO())
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.password,before)
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk,owner=self.user).exists())
