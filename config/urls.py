from django.contrib import admin
from django.urls import path
from main.views import home, services, works, about, contacts, privacy, contact_submit

urlpatterns = [
    path('', home, name='home'),
    path('services/', services, name='services'),
    path('works/', works, name='works'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('admin/', admin.site.urls),
    path("privacy/", privacy, name="privacy"),
    path("contact/submit/", contact_submit, name="contact_submit"),
]