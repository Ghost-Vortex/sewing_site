from django.db import models


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

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self):
        return self.title