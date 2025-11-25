from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from .models import Lead
from .forms import ContactForm
from .utils import send_telegram_message


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

    messages.success(request, "Запрос отправлен. Мы свяжемся с вами.")
    return redirect(request.META.get("HTTP_REFERER", "contacts"))


def home(request):
    # больше не обрабатываем POST, только рендер
    return render(request, "main/home.html")


def services(request):
    return render(request, "main/services.html")


def works(request):
    return render(request, "main/works.html")


def about(request):
    return render(request, "main/about.html")


def contacts(request):
    return render(request, "main/contacts.html")


def privacy(request):
    return render(request, "main/privacy.html")