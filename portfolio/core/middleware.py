# Middleware docs: https://docs.djangoproject.com/en/4.2/topics/http/middleware/

from os import urandom
from django.conf import settings


class CSPMiddleware:
    """Adds a Content-Security-Policy header to each response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.csp_nonce = urandom(16).hex()

        response = self.get_response(request)

        csp = (
            # most restrictive setting as default (fallback)
            "default-src 'none'; "
            # allow nonced inline scripts and external scripts from own origin
            f"script-src 'self' 'nonce-{request.csp_nonce}'; "
            # allow images from own origin
            "img-src 'self'; "
            # allow nonced inline CSS and external CSS from own origin
            f"style-src 'self' 'nonce-{request.csp_nonce}'; "
            # prevent <base href="https://attacker.com"> injection
            "base-uri 'self'; "
            # disallow framing the site to prevent clickjacking
            "frame-ancestors 'none'; "
            # form submission to this site only
            "form-action 'self'; "
            # TODO: report-to endpoint
        )

        # if we're in production, force TLS connection
        if not settings.DEBUG:
            csp += "upgrade-insecure-requests;"

        response["Content-Security-Policy"] = csp

        return response
