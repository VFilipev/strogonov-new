from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.models import SEOMixin


class EventType(SEOMixin):
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название типа мероприятия'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='URL-адрес',
        help_text='Уникальный URL-адрес для типа мероприятия'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Подробное описание типа мероприятия'
    )
    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    image_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1920, 1080)],
        format='WEBP',
        options={'quality': 85}
    )

    event_large_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(800, 600)],
        format='WEBP',
        options={'quality': 80}
    )
    event_card_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(400, 300)],
        format='WEBP',
        options={'quality': 75}
    )
    event_thumb_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(200, 150)],
        format='WEBP',
        options={'quality': 70}
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Тип мероприятия'
        verbose_name_plural = 'Типы мероприятий'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'slug': self.slug})

    def get_schema_org_json(self):
        schema = {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": self.title,
            "description": self.description[:500] if self.description else "",
        }

        if self.image:
            schema["image"] = self.image.url

        return schema


class EventCalculatorRequest(models.Model):

    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('done', 'Обработана'),
    ]

    contact_name = models.CharField(max_length=255, verbose_name='Имя')
    contact_phone = models.CharField(max_length=40, blank=True, verbose_name='Телефон')
    contact_email = models.EmailField(blank=True, verbose_name='E-mail')
    event_type = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Тип мероприятия (кириллица)',
    )
    payload = models.JSONField(verbose_name='JSON заявки')
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Заявка калькулятора мероприятия'
        verbose_name_plural = 'Заявки калькулятора мероприятия'
        ordering = ['-created_at']

    def __str__(self):
        label = self.event_type or 'Без типа'
        return f'{label} — {self.contact_name} ({self.created_at:%d.%m.%Y %H:%M})'
