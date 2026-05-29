from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static

from main.views import (
    home,
    services,
    works,
    about,
    contacts,
    privacy,
    contact_submit
)

from main.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}

handler404 = 'main.views.page_not_found'
handler500 = 'main.views.server_error'

urlpatterns = [
    # ---- Основные страницы ----
    path('', home, name='home'),
    path('services/', services, name='services'),
    path('works/', works, name='works'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),

    # ---- Обработка формы ----
    path('contact/submit/', contact_submit, name='contact_submit'),

    # ---- Политика конфиденциальности ----
    path("privacy/", privacy, name="privacy"),

    # ---- Админка ----
    path('admin/', admin.site.urls),

    # ---- robots.txt ----
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ),
        name="robots"
    ),

    # ---- Sitemap ----
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),

    # ---- Яндекс верификация ----
    path(
        "yandex_6a15f4e5e5c926a0.html",
        TemplateView.as_view(
            template_name="yandex_6a15f4e5e5c926a0.html",
            content_type="text/html"
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)