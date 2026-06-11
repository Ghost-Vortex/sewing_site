from django.conf import settings
from django.http import HttpResponsePermanentRedirect

CANONICAL_HOST = "ulagasheff.ru"


class CanonicalHostMiddleware:
    """301-редирект с www.ulagasheff.ru и с IP на основной домен.

    Дубль хоста (www / IP) размывает индексацию. Канонический хост — один.
    В DEBUG-режиме отключён, чтобы не мешать локальной разработке.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG:
            host = request.get_host().split(":")[0]
            if host != CANONICAL_HOST:
                return HttpResponsePermanentRedirect(
                    f"https://{CANONICAL_HOST}{request.get_full_path()}"
                )
        return self.get_response(request)
