from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, override_settings


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class PreviewTests(SimpleTestCase):
    def test_sections_are_available_and_explicitly_demo(self):
        for route in ("", "movimientos/", "sueldo/", "presupuesto/", "ahorros/", "obligaciones/", "revision/"):
            with self.subTest(route=route):
                response = self.client.get("/" + route)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Finanzas DAGD")
                self.assertContains(response, "Datos ficticios")
                self.assertContains(response, settings.APP_VERSION)

    def test_preview_cannot_accept_financial_writes(self):
        for route in ("/", "/movimientos/", "/sueldo/", "/obligaciones/"):
            with self.subTest(route=route):
                self.assertEqual(self.client.post(route, {"importe": "100"}).status_code, 405)

    def test_unknown_section_is_not_a_valid_screen(self):
        self.assertEqual(self.client.get("/desconocida/").status_code, 404)

    def test_filter_finds_demo_transaction_and_can_be_cleared(self):
        response = self.client.get("/movimientos/", {"q": "Arriendo"})
        self.assertContains(response, "Arriendo de octubre")
        self.assertNotContains(response, "Compra de mercado")
        self.assertContains(self.client.get("/movimientos/"), "Compra de mercado")

    def test_filter_empty_state_and_input_validation(self):
        self.assertContains(self.client.get("/movimientos/", {"q": "sin coincidencia"}), "Sin movimientos para estos filtros")
        self.assertEqual(self.client.get("/movimientos/", {"q": "a" * 81}).status_code, 400)
        self.assertEqual(self.client.get("/movimientos/", {"tipo": "inventado"}).status_code, 400)

    def test_transfer_filter_and_consolidated_balance_are_distinct(self):
        response = self.client.get("/movimientos/", {"tipo": "transferencia"})
        self.assertContains(response, "Reserva para emergencias")
        self.assertNotContains(response, "Arriendo de octubre")
        summary = self.client.get("/")
        self.assertEqual(summary.context["expenses"], 1350000)
        self.assertEqual(summary.context["balance"], 2650000)

    def test_search_does_not_render_injected_html(self):
        response = self.client.get("/movimientos/", {"q": '<script>alert(1)</script>'})
        self.assertNotContains(response, "<script>")
        self.assertContains(response, "&lt;script&gt;")

    def test_security_headers_and_local_hosts(self):
        response = self.client.get("/")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertIn("default-src 'none'", response.headers["Content-Security-Policy"])
        self.assertEqual(self.client.get("/", HTTP_HOST="externo.invalid").status_code, 400)

    def test_version_comes_from_single_file(self):
        self.assertEqual(settings.APP_VERSION, (Path(settings.BASE_DIR) / "VERSION").read_text().strip())

    def test_preview_has_no_database_file_to_create_on_startup(self):
        self.assertEqual(settings.DATABASES["default"]["NAME"], ":memory:")
