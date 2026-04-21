from django.db import models
from django.db.models import Max, Min
from django.utils.text import slugify
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.models import SEOMixin
from core.image_processors import SmartCropProcessor, NoOpProcessor


class LodgeType(SEOMixin):
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название типа размещения (например: Коттеджи)'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='URL-адрес',
        help_text='Уникальный URL-адрес для типа размещения'
    )
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Подзаголовок',
        help_text='Краткий подзаголовок для типа размещения'
    )
    hero_image = models.ImageField(
        upload_to='lodges/types/',
        blank=True,
        null=True,
        verbose_name='Главное изображение'
    )
    hero_image_webp = ImageSpecField(
        source='hero_image',
        processors=[ResizeToFill(1920, 1080)],
        format='WEBP',
        options={'quality': 85}
    )

    lodge_hero_main_webp = ImageSpecField(
        source='hero_image',
        processors=[SmartCropProcessor(1410, 940)],
        format='WEBP',
        options={'quality': 85}
    )
    lodge_hero_card_webp = ImageSpecField(
        source='hero_image',
        processors=[ResizeToFill(626, 456)],
        format='WEBP',
        options={'quality': 80}
    )
    lodge_hero_placeholder_webp = ImageSpecField(
        source='hero_image',
        processors=[NoOpProcessor()],
        format='WEBP',
        options={'quality': 50}
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Подробное описание типа размещения'
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
        verbose_name = 'Тип размещения'
        verbose_name_plural = 'Типы размещения'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        try:
            return reverse('lodges:type-detail', kwargs={'slug': self.slug})
        except:

            return f"/lodges/{self.slug}/"


class Lodge(SEOMixin):
    lodge_type = models.ForeignKey(
        LodgeType,
        on_delete=models.CASCADE,
        related_name='lodges',
        verbose_name='Тип размещения'
    )
    category = models.ForeignKey(
        'LodgeCategory',
        on_delete=models.SET_NULL,
        related_name='lodges',
        blank=True,
        null=True,
        verbose_name='Категория размещения'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название размещения (например: Коттедж №1)'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='URL-адрес',
        help_text='Уникальный URL-адрес для размещения'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Подробное описание размещения'
    )
    short_description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Краткое описание',
        help_text='Краткое описание для списков и превью'
    )
    capacity = models.PositiveIntegerField(
        verbose_name='Вместимость',
        help_text='Количество человек'
    )
    area = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Площадь',
        help_text='Площадь в квадратных метрах'
    )
    price_from = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Цена от',
        help_text='Минимальная цена за размещение'
    )
    location_description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание расположения',
        help_text='Описание расположения на территории базы'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )
    conveniences = models.TextField(
        blank=True,
        null=True,
        verbose_name='Удобства',
        help_text='Список удобств через запятую (например: Wi-Fi, отопление, кухня)'
    )
    include = models.TextField(
        blank=True,
        null=True,
        verbose_name='Включено в проживание',
        help_text='Что включено в стоимость проживания (например: Постельное белье, полотенца)'
    )
    bronirui_online_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='Ссылка на онлайн-бронирование',
        help_text='Если указана, кнопка «Забронировать» на сайте ведёт по этой ссылке'
    )

    class Meta:
        verbose_name = 'Размещение'
        verbose_name_plural = 'Размещения'
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.lodge_type.name} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        try:
            return reverse('lodges:detail', kwargs={'slug': self.slug})
        except:

            return f"/lodges/{self.slug}/"

    def get_schema_org_json(self):
        site_settings = None
        try:
            from core.models import SiteSettings
            site_settings = SiteSettings.objects.get()
        except Exception:
            pass

        schema = {
            "@context": "https://schema.org",
            "@type": "LodgingBusiness",
            "name": self.name,
            "description": self.short_description or self.description[:200] if self.description else "",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": site_settings.address if site_settings else ""
            }
        }

        if self.price_from:
            schema["priceRange"] = f"от {self.price_from} руб."

        if self.capacity:
            schema["numberOfRooms"] = str(self.capacity)

        return schema

    def get_breadcrumbs(self):
        breadcrumbs = [
            {
                "name": "Главная",
                "url": "/"
            },
            {
                "name": self.lodge_type.name,
                "url": self.lodge_type.get_absolute_url() if hasattr(self.lodge_type, 'get_absolute_url') else f"/lodges/{self.lodge_type.slug}/"
            },
            {
                "name": self.name,
                "url": self.get_absolute_url()
            }
        ]
        return breadcrumbs


class LodgeImage(models.Model):
    lodge = models.ForeignKey(
        Lodge,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Размещение'
    )
    image = models.ImageField(
        upload_to='lodges/images/',
        verbose_name='Изображение'
    )
    image_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1920, 1080)],
        format='WEBP',
        options={'quality': 85}
    )

    lodge_main_webp = ImageSpecField(
        source='image',
        processors=[SmartCropProcessor(1410, 940)],
        format='WEBP',
        options={'quality': 85}
    )
    lodge_card_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(626, 456)],
        format='WEBP',
        options={'quality': 80}
    )
    lodge_thumb_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 214)],
        format='WEBP',
        options={'quality': 75}
    )
    lodge_placeholder_webp = ImageSpecField(
        source='image',
        processors=[NoOpProcessor()],
        format='WEBP',
        options={'quality': 50}
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Alt текст',
        help_text='Альтернативный текст для изображения'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Изображение размещения'
        verbose_name_plural = 'Изображения размещения'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.lodge.name} - Изображение {self.order}'


class LodgeCategory(models.Model):
    lodge_type = models.ForeignKey(
        LodgeType,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Тип размещения'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название категории (например: На воде)'
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name='URL-адрес',
        help_text='Уникальный URL-адрес категории в рамках типа размещения'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to='lodges/categories/',
        blank=True,
        null=True,
        verbose_name='Фотография'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Категория размещения'
        verbose_name_plural = 'Категории размещения'
        ordering = ['order', 'name']
        constraints = [
            models.UniqueConstraint(fields=['lodge_type', 'slug'], name='unique_lodge_category_slug_per_type')
        ]

    def __str__(self):
        return f'{self.lodge_type.name} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_capacity_max(self):
        if hasattr(self, 'capacity_max') and self.capacity_max is not None:
            return self.capacity_max
        return self.lodges.filter(is_active=True).aggregate(value=Max('capacity'))['value'] or 0

    def get_price_from_min(self):
        if hasattr(self, 'price_from_min'):
            return self.price_from_min
        return self.lodges.filter(is_active=True).aggregate(value=Min('price_from'))['value']


class LodgePrice(models.Model):
    lodge = models.ForeignKey(
        Lodge,
        on_delete=models.CASCADE,
        related_name='price_set',
        verbose_name='Размещение'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название тарифа (например: Будни (1-2 чел.))'
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость',
        help_text='Стоимость в рублях'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )

    class Meta:
        verbose_name = 'Цена размещения'
        verbose_name_plural = 'Цены размещения'
        ordering = ['order', 'cost']

    def __str__(self):
        return f'{self.lodge.name} - {self.name}: {self.cost} руб.'


class LodgeAvailability(models.Model):
    lodge = models.ForeignKey(
        Lodge,
        on_delete=models.CASCADE,
        related_name='availability_set',
        verbose_name='Размещение'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Описание доступности (например: Доступен для бронирования)'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Доступность размещения'
        verbose_name_plural = 'Доступность размещения'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.lodge.name} - {self.name}'
