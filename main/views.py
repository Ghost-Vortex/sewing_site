from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, Http404

from .models import Lead, Work
from .forms import ContactForm
from .utils import send_telegram_message
from .services_data import SERVICES


def contact_submit(request):
    if request.method != "POST":
        return redirect("home")  # на всякий

    form = ContactForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Проверьте заполнение формы.")
        return redirect(request.META.get("HTTP_REFERER", "contacts"))

    name = form.cleaned_data["name"]
    contact = form.cleaned_data["contact"]
    message = form.cleaned_data.get("message") or "(без текста)"

    # --- Телега ---
    text = (
        "<b>Новый запрос с сайта Ulagasheff</b>\n\n"
        f"<b>Имя:</b> {name}\n"
        f"<b>Контакт:</b> {contact}\n"
        f"<b>Сообщение:</b> {message}"
    )

    sent_to_telegram = send_telegram_message(text)

    # --- Сохраним лид (если модель так называется) ---
    try:
        Lead.objects.create(
            name=name,
            phone=contact,   # если в модели поле phone
            comment=message, # если в модели поле comment
        )
    except Exception:
        pass

    # --- Фоллбэк на почту, если телега не ушла ---
    if not sent_to_telegram:
        email_to = getattr(settings, "CONTACT_EMAIL", None)
        if email_to:
            try:
                send_mail(
                    subject="Новый запрос с сайта Ulagasheff",
                    message=f"Имя: {name}\nКонтакт: {contact}\nСообщение: {message}",
                    from_email=getattr(
                        settings, "DEFAULT_FROM_EMAIL",
                        "no-reply@ulagasheff.com",
                    ),
                    recipient_list=[email_to],
                    fail_silently=True,
                )
            except Exception:
                pass

    # AJAX-запрос — вернём JSON
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "message": "Запрос отправлен. Мы свяжемся с вами в течение рабочего дня."})

    # Обычный POST (страница контактов без JS) — редирект с параметром, без Django messages
    return redirect("/contacts/?sent=1")


def home(request):
    return render(request, "main/home.html")


@cache_page(60 * 60)
def services(request):
    return render(request, "main/services.html", {"services_pages": SERVICES.values()})


@cache_page(60 * 60)
def service_detail(request, slug):
    service = SERVICES.get(slug)
    if service is None:
        raise Http404
    related = [SERVICES[s] for s in service["related"] if s in SERVICES]
    return render(
        request,
        "main/service_detail.html",
        {"service": service, "related": related},
    )


def works(request):
    works_qs = Work.objects.filter(is_active=True)
    return render(request, "main/works.html", {"works": works_qs})


@cache_page(60 * 60)
def about(request):
    return render(request, "main/about.html")


def contacts(request):
    return render(request, "main/contacts.html")


@cache_page(60 * 60 * 24)
def privacy(request):
    return render(request, "main/privacy.html")


def page_not_found(request, exception):
    return render(request, "404.html", status=404)


def server_error(request):
    return render(request, "500.html", status=500)