from django.conf import settings


def seo(request):
    """Передаёт SEO-настройки во все шаблоны (ID Яндекс.Метрики и т.п.)."""
    return {
        "YANDEX_METRIKA_ID": getattr(settings, "YANDEX_METRIKA_ID", ""),
    }
