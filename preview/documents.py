"""Lectura de dos documentos públicos explícitos; sin rutas de archivo del cliente."""
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_safe

DOCUMENTS = {
    "manual": ("MANUAL_USUARIO.md", "Manual de usuario"),
    "changelog": ("CHANGELOG.md", "Historial de cambios"),
}


@require_safe
def document(request, document):
    if document not in DOCUMENTS:
        raise Http404("Documento no disponible")
    filename, title = DOCUMENTS[document]
    try:
        content = (settings.BASE_DIR / filename).read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise Http404("Documento no disponible") from error
    return render(request, "preview/document.html", {"title": title, "filename": filename, "content": content})
