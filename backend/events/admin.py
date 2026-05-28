from django.contrib import admin
from .models import EventType, EventCalculatorRequest


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'title']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'is_active', 'order')
        }),
        ('Медиа', {
            'fields': ('image',)
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


@admin.register(EventCalculatorRequest)
class EventCalculatorRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_type', 'contact_name', 'contact_phone', 'contact_email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['event_type', 'contact_name', 'contact_phone', 'contact_email']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    fieldsets = (
        (None, {
            'fields': ('status', 'event_type', 'contact_name', 'contact_phone', 'contact_email', 'created_at'),
        }),
        ('Данные формы', {
            'fields': ('payload',),
        }),
    )
