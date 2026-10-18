class PreviewHeadersMiddleware:
    """La demostración no carga recursos externos ni permite ser embebida."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = (
            "default-src 'none'; style-src 'self'; img-src 'self'; "
            "font-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
        )
        if request.resolver_match and request.resolver_match.url_name == "document":
            response["Content-Security-Policy"] += "; script-src 'self'"
        response["Cache-Control"] = "no-store"
        response["X-Finanzas-DAGD"] = "local"
        return response
