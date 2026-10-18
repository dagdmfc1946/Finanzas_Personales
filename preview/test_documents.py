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

    def test_only_explicit_documents_are_available_and_unsafe_html_is_removed(self):
        self.assertEqual(self.client.get("/documentacion/secret/").status_code, 404)
        with patch("pathlib.Path.read_text", return_value="# Seguro\n\n<script>alert(1)</script>\n\n<img src=x onerror=alert(2)>\n\n[Malicioso](javascript:alert(3))"):
            response = self.client.get("/documentacion/manual/")
        self.assertContains(response, "<h1>Seguro</h1>")
        self.assertNotContains(response, "alert(1)")
        self.assertNotContains(response, "onerror")
        self.assertNotContains(response, "javascript:")
        self.assertNotContains(response, "<script>")

    def test_sidebar_links_open_new_tabs_with_safe_relationship(self):
        response = self.client.get("/demo/")
        self.assertContains(response, 'href="/documentacion/manual/" target="_blank" rel="noopener noreferrer"')
        self.assertContains(response, 'href="/documentacion/changelog/" target="_blank" rel="noopener noreferrer"')

    def test_markdown_renders_headings_lists_code_tables_and_links(self):
        source = "# Título\n\n## Sección\n\n**Importante** y `VERSION`.\n\n- Una cuenta\n- Otra cuenta\n\n```powershell\npython manage.py check\n```\n\n| Dato | Valor |\n| --- | --- |\n| Tipo | Local |\n\n[Fuente](https://example.com)"
        with patch("pathlib.Path.read_text", return_value=source):
            response = self.client.get("/documentacion/manual/")
        for html in ("<h1>Título</h1>", "<h2>Sección</h2>", "<strong>Importante</strong>", "<code>VERSION</code>", "<li>Una cuenta</li>", '<pre><code class="language-powershell">python manage.py check', "<table>", 'href="https://example.com"'):
            with self.subTest(html=html):
                self.assertContains(response, html)
        self.assertNotContains(response, "```powershell")

    def test_html_examples_inside_code_are_preserved_as_text(self):
        with patch("pathlib.Path.read_text", return_value="```html\n<script>ejemplo()</script>\n```"):
            response = self.client.get("/documentacion/manual/")
        self.assertContains(response, "&lt;script&gt;ejemplo()&lt;/script&gt;")
        self.assertNotContains(response, "<script>")
