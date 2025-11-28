from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

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
]