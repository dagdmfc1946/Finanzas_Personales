import hashlib
import json
import tempfile
import uuid
from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from .models import Activity, Account, Category, Entry
from .forms import CategoryForm, EntryForm
from .services import summary
from .backups import export_backup, restore_backup, canonical


@override_settings(ALLOWED_HOSTS=["testserver"])
class CategoryWorkflowTests(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user("grupos_ensayo")
        self.activity=Activity.objects.create(owner=self.user,name="Personal")
        self.account=Account.objects.create(owner=self.user,name="Banco",kind="banco")
        self.category=Category.objects.create(owner=self.user,name="Sueldo",kind="ingreso")
        self.client.force_login(self.user)

    def data(self,**changes):
        return {"kind":"inicial","date":"2026-10-08","description":"Saldo de ensayo","amount":"1234.50","activity":str(self.activity.pk),"account":str(self.account.pk),"category":"","destination_activity":"","destination_account":"","version":"0","submission":str(uuid.uuid4()),**changes}

    def test_groups_are_optional_and_do_not_affect_money(self):
        form=CategoryForm({"name":"Arriendo","kind":"gasto","group":" Gastos fijos "},user=self.user)
        self.assertTrue(form.is_valid(),form.errors)
        category=form.save()
        self.assertEqual(category.group,"Gastos fijos")
        self.assertIn("Gastos fijos",str(category))
        independent=CategoryForm({"name":"Ventas_Emprendimiento","kind":"ingreso","group":""},user=self.user)
        self.assertTrue(independent.is_valid(),independent.errors)
        self.assertEqual(independent.save().group,"")
        response=self.client.get("/app/organizacion/")
        self.assertContains(response,"Gastos fijos")
        self.assertContains(response,"Sin grupo")
        self.assertEqual(summary(self.user)["balance"],0)

    def test_initial_balance_error_is_on_category_and_explains_recovery(self):
        form=EntryForm(self.data(category=str(self.category.pk)),user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("category",form.errors)
        self.assertIn("sin categoría",str(form.errors["category"]).lower())
        response=self.client.post("/app/movimiento/nuevo/",self.data())
        self.assertEqual(response.status_code,302)
        self.assertEqual(Entry.objects.get().cents,123450)

    def test_income_mismatch_is_clear_and_valid_income_saves(self):
        expense=Category.objects.create(owner=self.user,name="Mercado",kind="gasto")
        form=EntryForm(self.data(kind="ingreso",category=str(expense.pk)),user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("category",form.errors)
        valid=EntryForm(self.data(kind="ingreso",category=str(self.category.pk)),user=self.user)
        self.assertTrue(valid.is_valid(),valid.errors)

    def test_backups_keep_groups_and_accept_v1_v2_categories(self):
        self.category.group="Trabajo"
        self.category.save()
        current=json.loads(export_backup(self.user))
        self.assertEqual(current["format"],3)
        with tempfile.TemporaryDirectory() as folder,override_settings(BACKUP_DIR=folder):
            restore_backup(self.user,canonical(current))
            self.assertEqual(Category.objects.get(pk=self.category.pk).group,"Trabajo")
            for version in (1,2):
                legacy=json.loads(json.dumps(current))
                legacy["format"]=version
                for row in legacy["objects"]["categories"]: row["fields"].pop("group")
                if version==1:
                    for key in ("salaries","salary_receipts"): legacy["objects"].pop(key)
                legacy.pop("sha256")
                legacy["sha256"]=hashlib.sha256(canonical(legacy)).hexdigest()
                restore_backup(self.user,canonical(legacy))
                self.assertEqual(Category.objects.get(pk=self.category.pk).group,"")

    def test_only_entry_forms_allow_the_local_script(self):
        response=self.client.get("/app/movimiento/nuevo/")
        self.assertContains(response,"ledger/entry_form.js")
        self.assertContains(response,'id="entry-kind-help"',count=1)
        self.assertIn("script-src 'self'",response["Content-Security-Policy"])
        self.assertNotIn("script-src",self.client.get("/app/resumen/")["Content-Security-Policy"])
