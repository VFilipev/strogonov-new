from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from core.models import SEOMixin


class Activity(SEOMixin):

    CATEGORY_CHOICES = [
        ('active', 'Активный отдых'),
        ('peaceful', 'Спокойный отдых'),
    ]

    SEASON_CHOICES = [
        ('winter', 'Зима'),
        ('summer', 'Лето'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория',
        help_text='Тип активности'
    )
    season = models.CharField(
        max_length=20,
        choices=SEASON_CHOICES,
        blank=True,
        null=True,
        verbose_name='Сезон',
        help_text='Сезон активности (зима или лето)'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название активности'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='URL-адрес',
        help_text='Уникальный URL-адрес для активности'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text=(
            'Поддерживается разметка: *курсив*, **жирный**, '
            '***жирный курсив***. Переносы строк сохраняются.'
        )
    )
    short_description = models.CharField(
        max_length=300,
        blank=True,
        default='',
        verbose_name='Краткое описание',
        help_text='Короткий текст для лицевой стороны карточки'
    )
    image = models.ImageField(
        upload_to='activities/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    image_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFit(1920, 1920, upscale=False)],
        format='WEBP',
        options={'quality': 85}
    )
    image_position_x = models.PositiveSmallIntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Фокус изображения по горизонтали, %',
        help_text='0 — левый край, 50 — центр, 100 — правый край',
    )
    image_position_y = models.PositiveSmallIntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Фокус изображения по вертикали, %',
        help_text='0 — верхний край, 50 — центр, 100 — нижний край',
    )
    video = models.FileField(
        upload_to='activities/videos/',
        blank=True,
        null=True,
        verbose_name='Видео',
        help_text='Видеофайл для активности'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )
    page_path = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Ссылка на страницу',
        help_text='путь вида /sauna',
    )

    class Meta:
        verbose_name = 'Активность'
        verbose_name_plural = 'Активности'
        ordering = ['category', 'season', 'order', 'title']

    def __str__(self):
        return f'{self.get_category_display()} - {self.title}'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('activities:detail', kwargs={'slug': self.slug})
