import re

from django.db import models

_TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}


def slugify_ru(text):
    """Кириллица -> латинский slug: «Туника удлинённая» -> tunika-udlinennaya."""
    text = text.lower()
    text = ''.join(_TRANSLIT.get(ch, ch) for ch in text)
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:200] or 'work'


class Lead(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.phone}"


class Work(models.Model):
    CATEGORY_CHOICES = [
        ('outerwear', 'Outerwear'),
        ('capsule', 'Capsule'),
        ('drop', 'Drop'),
        ('merch', 'Merch'),
    ]

    WIDE_CHOICES = [
        ('normal', 'Обычная'),
        ('wide', 'Широкая (2 колонки)'),
    ]

    title = models.CharField('Название', max_length=200)
    description = models.CharField('Описание', max_length=300, blank=True)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES, default='drop')
    image = models.ImageField('Фото', upload_to='works/')
    card_size = models.CharField('Размер карточки', max_length=10, choices=WIDE_CHOICES, default='normal')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Показывать', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # --- Поля кейса (страница /works/<slug>/) ---
    slug = models.SlugField('URL (заполняется само)', max_length=220, unique=True, null=True, blank=True)
    fabric = models.CharField('Ткань', max_length=200, blank=True, help_text='Например: футер 3-нитка с начёсом')
    quantity = models.CharField('Тираж', max_length=100, blank=True, help_text='Например: 300 ед.')
    lead_time = models.CharField('Срок', max_length=100, blank=True, help_text='Например: 14 рабочих дней')
    body = models.TextField('Текст кейса', blank=True, help_text='Задача, решение, детали. Пустая строка = новый абзац.')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Авто-slug + сжатие фото до 1920px по длинной стороне."""
        if not self.slug and self.title:
            base = slugify_ru(self.title)
            slug = base
            n = 2
            while Work.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)
        if self.image:
            try:
                from PIL import Image
                path = self.image.path
                img = Image.open(path)
                if max(img.size) > 1920:
                    img.thumbnail((1920, 1920), Image.LANCZOS)
                    save_kwargs = {"optimize": True}
                    if (img.format or "").upper() in ("JPEG", "WEBP"):
                        save_kwargs["quality"] = 82
                    img.save(path, **save_kwargs)
            except Exception:
                pass