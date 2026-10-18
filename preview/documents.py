"""Lectura de dos documentos públicos explícitos; sin rutas de archivo del cliente."""
import markdown
import nh3
from markdown.extensions.toc import slugify
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_safe

DOCUMENTS = {
    "manual": ("MANUAL_USUARIO.md", "Manual de usuario"),
    "changelog": ("CHANGELOG.md", "Historial de cambios"),
}


def heading_slug(value, separator):
    return "doc-" + slugify(value, separator)


def render_markdown(source):
    parser = markdown.Markdown(
        extensions=["markdown.extensions.fenced_code", "markdown.extensions.tables", "markdown.extensions.sane_lists", "markdown.extensions.toc"],
        extension_configs={"markdown.extensions.toc": {"marker": "", "slugify": heading_slug}},
        output_format="html",
    )
    html = parser.convert(source)
    return sanitize_html(html), sanitize_html(parser.toc)


def sanitize_html(html):
    # Solo este resultado saneado se marca como HTML en la plantilla.
    return nh3.clean(
        html,
        tags={"p", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "em", "ul", "ol", "li", "pre", "code", "blockquote", "hr", "br", "a", "table", "thead", "tbody", "tr", "th", "td"},
        attributes={"a": {"href", "title"}, "code": {"class"}, "ol": {"start"}, **{f"h{level}": {"id"} for level in range(1, 7)}},
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
    content_html, toc_html = render_markdown(content)
    return render(request, "preview/document.html", {"title": title, "filename": filename, "content_html": content_html, "toc_html": toc_html})
