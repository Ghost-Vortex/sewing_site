import requests
from django.conf import settings


def send_telegram_message(text: str) -> bool:
    """
    Отправка сообщения в Telegram-чат.
    Нужно в settings.py задать TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID.
    Возвращает True, если ушло без ошибок.
    """
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", None)

    if not token or not chat_id:
        return False  # телега не настроена

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    try:
        resp = requests.post(url, data=payload, timeout=10)
        return resp.status_code == 200
    except Exception:
        return False
