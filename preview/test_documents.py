from unittest.mock import patch
from django.test import SimpleTestCase, override_settings


@override_settings(ALLOWED_HOSTS=["testserver"])
class DocumentTests(SimpleTestCase):
    def test_manual_and_changelog_are_readable_without_creating_a_user(self):
        for name, filename in (("manual", "MANUAL_USUARIO.md"), ("changelog", "CHANGELOG.md")):
            with self.subTest(document=name):
                response = self.client.get(f"/documentacion/{name}/")
                self.assertContains(response, filename)
                self.assertContains(response, "Finanzas DAGD")
                self.assertEqual(self.client.post(f"/documentacion/{name}/").status_code, 405)

    def test_only_explicit_documents_are_available_and_html_is_escaped(self):
        self.assertEqual(self.client.get("/documentacion/secret/").status_code, 404)
        with patch("pathlib.Path.read_text", return_value="<script>alert(1)</script>"):
            response = self.client.get("/documentacion/manual/")
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, "<script>")

    def test_sidebar_links_open_new_tabs_with_safe_relationship(self):
        response = self.client.get("/demo/")
        self.assertContains(response, 'href="/documentacion/manual/" target="_blank" rel="noopener noreferrer"')
        self.assertContains(response, 'href="/documentacion/changelog/" target="_blank" rel="noopener noreferrer"')
