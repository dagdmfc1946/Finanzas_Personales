"""Lectura de dos documentos públicos explícitos; sin rutas de archivo del cliente."""
import markdown
import nh3
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_safe

DOCUMENTS = {
    "manual": ("MANUAL_USUARIO.md", "Manual de usuario"),
    "changelog": ("CHANGELOG.md", "Historial de cambios"),
}


def render_markdown(source):
    html = markdown.markdown(source, extensions=["markdown.extensions.fenced_code", "markdown.extensions.tables", "markdown.extensions.sane_lists"], output_format="html")
    # Solo este resultado saneado se marca como HTML en la plantilla.
    return nh3.clean(
        html,
        tags={"p", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "em", "ul", "ol", "li", "pre", "code", "blockquote", "hr", "br", "a", "table", "thead", "tbody", "tr", "th", "td"},
        attributes={"a": {"href", "title"}, "code": {"class"}, "ol": {"start"}},
        url_schemes={"http", "https", "mailto"},
    )


@require_safe
def document(request, document):
    if document not in DOCUMENTS:
        raise Http404("Documento no disponible")
    filename, title = DOCUMENTS[document]
    try:
        content = (settings.BASE_DIR / filename).read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise Http404("Documento no disponible") from error
    return render(request, "preview/document.html", {"title": title, "filename": filename, "content_html": render_markdown(content)})
