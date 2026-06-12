from django.contrib import admin
from .models import Lead, Work

admin.site.register(Lead)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'card_size', 'order', 'is_active']
    list_editable = ['order', 'is_active', 'card_size']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['slug']
    fieldsets = (
        (None, {'fields': ('title', 'description', 'category', 'image', 'card_size', 'order', 'is_active')}),
        ('Кейс (страница работы)', {
            'fields': ('slug', 'fabric', 'quantity', 'lead_time', 'body'),
            'description': 'Заполните — у работы появится своя страница /works/…/ с этим текстом.',
        }),
    )
