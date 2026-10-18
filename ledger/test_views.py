import tempfile
import uuid
from pathlib import Path
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.utils import timezone
from .models import Activity, Account, Category, Entry, Installation
from .services import summary
from .services import save_entry, void_entry


@override_settings(ALLOWED_HOSTS=["testserver"])
class AccessTests(TestCase):
    def test_first_setup_creates_only_one_user_and_no_financial_examples(self):
        self.assertRedirects(self.client.get("/"), "/configurar/", fetch_redirect_response=False)
        response = self.client.post("/configurar/", {"username": "prueba", "password1": "Ensayo-local!972", "password2": "Ensayo-local!972"})
        self.assertRedirects(response, "/app/")
        self.assertEqual(Installation.objects.count(), 1)
        self.assertTrue(get_user_model().objects.get(username="prueba").is_staff)
        self.assertEqual(Entry.objects.count(), 0)
        self.assertEqual(Activity.objects.count(), 1)
        self.client.logout()
        self.assertRedirects(self.client.post("/acceso/", {"username": "prueba", "password": "Ensayo-local!972"}), "/app/")
        self.assertRedirects(self.client.post("/salir/"), "/acceso/")
        self.assertRedirects(self.client.get("/configurar/"), "/acceso/", fetch_redirect_response=False)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_anonymous_write_is_protected_and_setup_has_csrf(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post("/configurar/", {}).status_code, 403)
        self.assertEqual(self.client.get("/app/").status_code, 302)
        self.assertEqual(self.client.post("/app/movimiento/nuevo/", {}).status_code, 302)


@override_settings(ALLOWED_HOSTS=["testserver"])
class LedgerViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("ensayo", password="Ensayo-local!972")
        Installation.objects.create(user=self.user)
        self.activity = Activity.objects.create(owner=self.user, name="Personal")
        self.account = Account.objects.create(owner=self.user, name="Efectivo", kind="efectivo")
        self.client.force_login(self.user)

    def data(self, **changes):
        return {"submission": str(uuid.uuid4()), "version": "0", "kind": "ingreso", "date": "2026-10-17", "description": "Ensayo sintético", "activity": str(self.activity.pk), "account": str(self.account.pk), "amount": "10.01", **changes}

    def test_all_sections_and_forms_render(self):
        for path in ("/app/", "/app/movimientos/", "/app/organizacion/", "/app/historial/", "/app/respaldo/", "/app/revision/", "/app/movimiento/nuevo/", "/app/catalogo/actividad/nuevo/", "/app/catalogo/cuenta/nuevo/", "/app/catalogo/categoria/nuevo/", "/clave/"):
            with self.subTest(path=path):
                self.assertContains(self.client.get(path), "Finanzas DAGD")

    def test_new_entry_date_defaults_to_today(self):
        response = self.client.get("/app/movimiento/nuevo/")
        self.assertEqual(response.context["form"]["date"].value(), timezone.localdate())

    def test_money_duplicate_submission_correction_and_void(self):
        data = self.data()
        self.assertEqual(self.client.post("/app/movimiento/nuevo/", data).status_code, 302)
        self.assertEqual(self.client.post("/app/movimiento/nuevo/", data).status_code, 400)
        self.assertEqual(Entry.objects.count(), 1)
        entry = Entry.objects.get()
        self.assertEqual(entry.cents, 1001)
        edit = self.data(submission=str(entry.pk), version="1", amount="20.25", reason="Corregir ensayo")
        self.assertEqual(self.client.post(f"/app/movimiento/{entry.pk}/", edit).status_code, 302)
        self.assertEqual(self.client.post(f"/app/movimiento/{entry.pk}/", edit).status_code, 400)
        self.assertEqual(summary(self.user)["balance"], 2025)
        self.assertEqual(self.client.post(f"/app/movimiento/{entry.pk}/anular/", {"version": 2, "reason": "Finalizar ensayo", "confirm": "on"}).status_code, 302)
        self.assertEqual(summary(self.user)["balance"], 0)
        self.assertEqual(Entry.objects.count(), 1)

    def test_invalid_money_transfer_and_other_owner_are_rejected(self):
        other = get_user_model().objects.create_user("otro")
        private = Account.objects.create(owner=other, name="Otra", kind="banco")
        for changes in ({"amount": "0"}, {"amount": "1.001"}, {"kind": "transferencia"}, {"account": str(private.pk)}):
            with self.subTest(changes=changes):
                self.assertEqual(self.client.post("/app/movimiento/nuevo/", self.data(**changes)).status_code, 400)
        self.assertEqual(Entry.objects.count(), 0)
        self.assertEqual(self.client.get(f"/app/catalogo/cuenta/{private.pk}/").status_code, 404)

    def test_initial_account_and_category_type_guard(self):
        response = self.client.post("/app/catalogo/cuenta/nuevo/", {"name": "Ahorro", "kind": "ahorro", "initial_amount": "30.10", "initial_activity": str(self.activity.pk)})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(summary(self.user)["balance"], 3010)
        category = Category.objects.create(owner=self.user, name="Trabajo", kind="ingreso")
        self.client.post("/app/movimiento/nuevo/", self.data(category=str(category.pk)))
        self.assertEqual(self.client.post(f"/app/catalogo/categoria/{category.pk}/", {"name": "Trabajo", "kind": "gasto"}).status_code, 400)

    def test_filters_match_transfer_destination_and_exclude_voided_entries(self):
        destination = Activity.objects.create(owner=self.user, name="Taller")
        transfer = Entry(owner=self.user, date="2026-10-17", description="Aporte sintético", kind="transferencia", cents=100, activity=self.activity, account=self.account, destination_activity=destination, destination_account=self.account)
        save_entry(transfer, self.user)
        path = "/app/movimientos/"
        self.assertContains(self.client.get(path, {"activity": str(destination.pk), "q": "Aporte", "start": "2026-10-17", "end": "2026-10-17"}), "Aporte sintético")
        self.assertNotContains(self.client.get(path, {"start": "2026-10-18"}), "Aporte sintético")
        self.assertEqual(self.client.get(path, {"start": "2026-10-18", "end": "2026-10-17"}).status_code, 400)
        void_entry(transfer, self.user, 1, "Ensayo de filtro")
        self.assertNotContains(self.client.get(path), "Aporte sintético")
        self.assertContains(self.client.get(path, {"void": "on"}), "Aporte sintético")

    def test_download_requires_post_and_csrf_and_logout_requires_post(self):
        self.assertEqual(self.client.get("/app/respaldo/descargar/").status_code, 405)
        self.assertEqual(self.client.get("/salir/").status_code, 405)
        protected = Client(enforce_csrf_checks=True)
        protected.force_login(self.user)
        self.assertEqual(protected.post("/app/respaldo/descargar/").status_code, 403)
        with tempfile.TemporaryDirectory() as folder, override_settings(BACKUP_DIR=Path(folder)):
            response = self.client.post("/app/respaldo/descargar/")
            self.assertEqual(response.status_code, 200)
            self.assertIn("attachment", response.headers["Content-Disposition"])
            self.assertEqual(len(list((Path(folder) / f"usuario-{self.user.pk}").glob("*.json"))), 1)
