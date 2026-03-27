from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin
from .models import SiteSettings, Statistic, GalleryImage, HeroSection, HeroImage, GuestFeedback, AfishaEvent


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):

    fieldsets = (
        ('Состояние сайта', {
            'fields': ('site_active',),
            'description': 'При снятии галочки главная страница уходит в режим технического обслуживания.',
        }),
        ('Навигация', {
            'fields': ('nav_show_services', 'nav_show_tours'),
            'description': 'Видимость пунктов «Услуги» и «Туры» в шапке и связанных блоках.',
        }),
        ('Основная информация', {
            'fields': ('site_name', 'logo', 'phone_primary', 'phone_secondary', 'email', 'address')
        }),
        ('Социальные сети', {
            'fields': ('telegram_url', 'vk_url')
        }),
        ('Реестр', {
            'fields': ('registry_number', 'registry_url')
        }),
        ('Главная страница', {
            'fields': ('hero_image', 'hero_title', 'hero_subtitle')
        }),
        ('План базы', {
            'fields': ('base_plan_image', 'base_plan_description')
        }),
        ('Логотипы', {
            'fields': ('national_projects_logo',)
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'og_title', 'og_description', 'og_image',
                'canonical_url', 'robots_meta'
            )
        }),
    )


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ['number', 'label', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['number', 'label', 'description']
    ordering = ['order', 'id']

    fieldsets = (
        ('Основная информация', {
            'fields': ('number', 'label', 'description', 'is_active', 'order')
        }),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):

    list_display = ['alt_text', 'position', 'column', 'is_active', 'order', 'image_preview']
    list_filter = ['position', 'column', 'is_active']
    search_fields = ['alt_text']
    ordering = ['position', 'column', 'order', 'id']

    fieldsets = (
        ('Основная информация', {
            'fields': ('image', 'alt_text', 'position', 'column', 'is_active', 'order')
        }),
    )

    def image_preview(self, obj):

        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Превью'


class HeroImageInline(admin.TabularInline):
    model = HeroImage
    extra = 1
    fields = ['image', 'alt_text', 'order', 'is_active', 'transition_duration']
    ordering = ['order']


@admin.action(description='Активировать выбранные Hero секции')
def activate_hero(modeladmin, request, queryset):
    HeroSection.objects.filter(is_active=True).update(is_active=False)
    queryset.update(is_active=True)


@admin.action(description='Деактивировать выбранные Hero секции')
def deactivate_hero(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_type', 'is_active', 'order']
    list_filter = ['display_type', 'is_active']
    search_fields = ['title', 'subtitle']
    inlines = [HeroImageInline]
    ordering = ['order', 'id']
    actions = [activate_hero, deactivate_hero]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'subtitle', 'display_type', 'is_active', 'order')
        }),
        ('Медиа', {
            'fields': ('preview_image', 'promo_video', 'video_poster')
        }),
        ('Настройки видео', {
            'classes': ('collapse',),
            'fields': ('autoplay_video', 'loop_video', 'mute_video')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'og_title', 'og_description', 'og_image',
                'canonical_url', 'robots_meta'
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, str(e), level='error')
            raise


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ['hero_section', 'alt_text', 'is_active', 'order', 'transition_duration', 'image_preview']
    list_filter = ['hero_section', 'is_active']
    search_fields = ['alt_text', 'hero_section__title']
    ordering = ['hero_section', 'order', 'id']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Превью'


@admin.register(AfishaEvent)
class AfishaEventAdmin(admin.ModelAdmin):

    list_display = ['title', 'category', 'event_date', 'price_per_guest', 'is_active']
    list_filter = ['category', 'is_active', 'event_date']
    search_fields = ['title', 'description']
    ordering = ['event_date', 'id']
    date_hierarchy = 'event_date'

    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'event_date', 'is_active'),
        }),
        ('Описание', {
            'fields': ('description',),
        }),
        ('Цена', {
            'fields': ('price_per_guest',),
        }),
        ('Медиа', {
            'fields': ('image',),
        }),
    )


@admin.register(GuestFeedback)
class GuestFeedbackAdmin(admin.ModelAdmin):

    list_display = ['id', 'topic', 'name', 'email', 'phone', 'created_at']
    list_filter = ['topic', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    fieldsets = (
        (None, {
            'fields': ('topic', 'name', 'email', 'phone', 'created_at'),
        }),
        ('Визит', {
            'fields': ('visit_date', 'visit_time'),
        }),
        ('Сообщение', {
            'fields': ('message', 'attachment'),
        }),
    )
