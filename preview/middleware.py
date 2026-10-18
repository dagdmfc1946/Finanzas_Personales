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
        response["Cache-Control"] = "no-store"
        return response
