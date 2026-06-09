from datetime import timedelta

from django.db import models
from django.db.models import Sum
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from solo.models import SingletonModel

from core.models import SEOMixin


class Instructor(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя')
    role = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Роль',
        help_text='Например: Ведущий гид, Механик и гид',
    )
    bio = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(
        upload_to='tours/instructors/',
        blank=True,
        null=True,
        verbose_name='Фото',
    )
    photo_webp = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(600, 600)],
        format='WEBP',
        options={'quality': 80},
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Учитывается в расчёте доступных слотов.',
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')

    class Meta:
        verbose_name = 'Инструктор'
        verbose_name_plural = 'Инструкторы'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Route(SEOMixin):

    DIFFICULTY_CHOICES = [
        ('easy', 'Лёгкая'),
        ('medium', 'Средняя'),
        ('hard', 'Тяжёлая'),
    ]

    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL-адрес')
    description = models.TextField(blank=True, verbose_name='Описание')

    duration_minutes = models.PositiveIntegerField(
        verbose_name='Длительность (минут)',
        help_text='Используется для расчёта слотов и занятости инструктора/техники.',
    )
    duration_label = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Длительность (текст)',
        help_text='Например: «2,5 - 3 часа». Для показа на сайте.',
    )
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        verbose_name='Сложность',
    )
    min_vehicles = models.PositiveIntegerField(
        default=1,
        verbose_name='Минимум квадроциклов для выезда',
        help_text='Если суммарно по заявкам набрано меньше — проведение не гарантируется.',
    )
    group_label = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Группа (текст)',
        help_text='Например: «от 3 квадроциклов». Только для показа; ограничение задаётся в «Минимум квадроциклов».',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
        help_text='Стоимость за один квадроцикл при разовой брони.',
    )
    photo = models.ImageField(
        upload_to='tours/routes/',
        blank=True,
        null=True,
        verbose_name='Фото',
    )
    image_webp = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(1920, 1080)],
        format='WEBP',
        options={'quality': 85},
    )
    route_large_webp = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(800, 600)],
        format='WEBP',
        options={'quality': 80},
    )
    route_card_webp = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(400, 300)],
        format='WEBP',
        options={'quality': 75},
    )

    # --- Поля для тура выходного дня ---
    available_for_tour = models.BooleanField(
        default=False,
        verbose_name='Доступен для тура выходного дня',
    )
    tour_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Цена в составе тура',
    )
    tour_old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Старая цена тура',
        help_text='Зачёркнутая «обычная цена».',
    )
    tour_description = models.TextField(
        blank=True,
        verbose_name='Описание в туре',
    )
    tour_outing_start = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Время выезда в туре (начало)',
        help_text='Время выезда в субботу для тура выходного дня. Например 10:00.',
    )
    tour_outing_end = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Время выезда в туре (конец)',
        help_text='Например 12:00. Используется для занятости в субботу.',
    )

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class WeekendTourProgram(SingletonModel, SEOMixin):

    intro = models.TextField(blank=True, verbose_name='Вступительный текст')
    benefits = models.JSONField(
        default=list, blank=True, verbose_name='Преимущества',
        help_text='Список: [{"title": "...", "text": "..."}].',
    )
    schedule = models.JSONField(
        default=list, blank=True, verbose_name='Программа по дням',
        help_text='Список: [{"day": "Пятница", "items": ["...", "..."]}].',
    )
    included_items = models.JSONField(
        default=list, blank=True, verbose_name='Включено в тур',
        help_text='Список: [{"title": "...", "text": "..."}].',
    )
    experience_items = models.JSONField(
        default=list, blank=True, verbose_name='Блоки впечатлений',
        help_text='Список: [{"id": "...", "title": "...", "text": "..."}].',
    )

    class Meta:
        verbose_name = 'Тур выходного дня (контент)'
        verbose_name_plural = 'Тур выходного дня (контент)'

    def __str__(self):
        return 'Тур выходного дня'


class BookingSettings(SingletonModel):

    MODE_CHOICES = [
        ('strict', 'Строгий (нельзя оставить заявку без свободного ресурса)'),
        ('lite', 'Лайт (заявку можно оставить даже без свободного ресурса)'),
    ]

    booking_mode = models.CharField(
        max_length=10, choices=MODE_CHOICES, default='lite',
        verbose_name='Режим бронирования',
    )
    work_day_start = models.TimeField(default='09:00', verbose_name='Начало рабочего дня')
    work_day_end = models.TimeField(default='19:00', verbose_name='Конец рабочего дня')
    slot_step_minutes = models.PositiveIntegerField(default=30, verbose_name='Шаг сетки слотов (минут)')
    instructor_count_override = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name='Кол-во инструкторов (ручное)',
        help_text='Если пусто — считается по числу активных инструкторов.',
    )
    quad_fleet_size = models.PositiveIntegerField(
        default=0,
        verbose_name='Парк квадроциклов (всего)',
        help_text='Сколько квадроциклов всего. 0 — не учитывать лимит техники.',
    )

    class Meta:
        verbose_name = 'Настройки бронирования'
        verbose_name_plural = 'Настройки бронирования'

    def __str__(self):
        return 'Настройки бронирования'

    def get_instructor_count(self):
        if self.instructor_count_override is not None:
            return self.instructor_count_override
        return Instructor.objects.filter(is_active=True).count()


class OutingQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(status='cancelled')

    def overlapping(self, start_at, end_at):
        return self.filter(start_at__lt=end_at, end_at__gt=start_at)


class Outing(models.Model):

    TYPE_CHOICES = [
        ('route', 'Маршрут'),
        ('weekend_tour', 'Тур выходного дня'),
    ]
    STATUS_CHOICES = [
        ('forming', 'Набор группы'),
        ('confirmed', 'Подтверждён'),
        ('cancelled', 'Отменён'),
        ('done', 'Завершён'),
    ]

    route = models.ForeignKey(
        Route, on_delete=models.PROTECT, related_name='outings', verbose_name='Маршрут',
    )
    booking_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default='route', verbose_name='Тип',
    )
    start_at = models.DateTimeField(verbose_name='Начало')
    end_at = models.DateTimeField(verbose_name='Окончание')
    duration_minutes = models.PositiveIntegerField(verbose_name='Длительность (минут)')
    checkin_date = models.DateField(
        blank=True, null=True, verbose_name='Дата заезда (тур)',
        help_text='Пятница для тура выходного дня.',
    )
    instructor = models.ForeignKey(
        Instructor, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='outings', verbose_name='Инструктор',
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='forming', verbose_name='Статус',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    objects = OutingQuerySet.as_manager()

    class Meta:
        verbose_name = 'Выезд'
        verbose_name_plural = 'Выезды'
        ordering = ['-start_at']
        indexes = [
            models.Index(fields=['start_at', 'end_at']),
            models.Index(fields=['route', 'start_at', 'booking_type']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f'{self.get_booking_type_display()} «{self.route.title}» — {self.start_at:%d.%m.%Y %H:%M}'

    def save(self, *args, **kwargs):
        if self.start_at and self.duration_minutes and not self.end_at:
            self.end_at = self.start_at + timedelta(minutes=self.duration_minutes)
        super().save(*args, **kwargs)

    @property
    def total_vehicles(self):
        agg = self.bookings.exclude(status='cancelled').aggregate(s=Sum('vehicles_count'))
        return agg['s'] or 0

    @property
    def total_people(self):
        agg = self.bookings.exclude(status='cancelled').aggregate(s=Sum('people_count'))
        return agg['s'] or 0

    @property
    def min_vehicles(self):
        return self.route.min_vehicles

    @property
    def meets_minimum(self):
        return self.total_vehicles >= self.route.min_vehicles

    @property
    def vehicles_needed(self):
        return max(0, self.route.min_vehicles - self.total_vehicles)


class Booking(models.Model):

    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('cancelled', 'Отменена'),
    ]

    outing = models.ForeignKey(
        Outing, on_delete=models.CASCADE, related_name='bookings', verbose_name='Выезд',
    )
    vehicles_count = models.PositiveIntegerField(default=1, verbose_name='Кол-во квадроциклов')
    people_count = models.PositiveIntegerField(blank=True, null=True, verbose_name='Кол-во человек')

    contact_name = models.CharField(max_length=255, verbose_name='Имя')
    contact_phone = models.CharField(max_length=40, blank=True, verbose_name='Телефон')
    contact_email = models.EmailField(blank=True, verbose_name='E-mail')

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус',
    )
    over_capacity = models.BooleanField(
        default=False,
        verbose_name='Сверх ёмкости ресурсов',
        help_text='Заявка оставлена в лайт-режиме без свободного инструктора/техники.',
    )
    mode_at_creation = models.CharField(max_length=10, blank=True, verbose_name='Режим при создании')
    payload = models.JSONField(default=dict, blank=True, verbose_name='Доп. данные')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['status'])]

    def __str__(self):
        return f'{self.contact_name} — {self.vehicles_count} квад. ({self.outing})'
