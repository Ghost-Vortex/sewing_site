import re

from django.db import migrations, models

_TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}


def _slugify_ru(text):
    text = text.lower()
    text = ''.join(_TRANSLIT.get(ch, ch) for ch in text)
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:200] or 'work'


def fill_slugs(apps, schema_editor):
    Work = apps.get_model('main', 'Work')
    seen = set(
        Work.objects.exclude(slug=None).values_list('slug', flat=True)
    )
    for work in Work.objects.filter(slug=None):
        base = _slugify_ru(work.title)
        slug = base
        n = 2
        while slug in seen:
            slug = f"{base}-{n}"
            n += 1
        work.slug = slug
        seen.add(slug)
        work.save(update_fields=['slug'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='slug',
            field=models.SlugField(blank=True, max_length=220, null=True, unique=True, verbose_name='URL (заполняется само)'),
        ),
        migrations.AddField(
            model_name='work',
            name='fabric',
            field=models.CharField(blank=True, help_text='Например: футер 3-нитка с начёсом', max_length=200, verbose_name='Ткань'),
        ),
        migrations.AddField(
            model_name='work',
            name='quantity',
            field=models.CharField(blank=True, help_text='Например: 300 ед.', max_length=100, verbose_name='Тираж'),
        ),
        migrations.AddField(
            model_name='work',
            name='lead_time',
            field=models.CharField(blank=True, help_text='Например: 14 рабочих дней', max_length=100, verbose_name='Срок'),
        ),
        migrations.AddField(
            model_name='work',
            name='body',
            field=models.TextField(blank=True, help_text='Задача, решение, детали. Пустая строка = новый абзац.', verbose_name='Текст кейса'),
        ),
        migrations.RunPython(fill_slugs, noop),
    ]
