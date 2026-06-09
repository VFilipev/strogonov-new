from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import (
    Booking,
    BookingSettings,
    Instructor,
    Outing,
    Route,
    WeekendTourProgram,
)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'is_active', 'order']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['name', 'role']
    ordering = ['order', 'name']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'difficulty', 'duration_label', 'min_vehicles', 'price',
        'available_for_tour', 'is_active', 'order',
    ]
    list_filter = ['is_active', 'available_for_tour', 'difficulty']
    list_editable = ['is_active', 'available_for_tour', 'order']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'title']

    fieldsets = (
        ('Основное', {
            'fields': (
                'title', 'slug', 'description', 'photo', 'difficulty',
                'duration_minutes', 'duration_label',
                'min_vehicles', 'group_label', 'price', 'is_active', 'order',
            )
        }),
        ('Тур выходного дня', {
            'fields': (
                'available_for_tour', 'tour_price', 'tour_old_price',
                'tour_description', 'tour_outing_start', 'tour_outing_end',
            )
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'og_title', 'og_description', 'og_image',
                'canonical_url', 'robots_meta',
            )
        }),
    )


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = [
        'contact_name', 'contact_phone', 'vehicles_count', 'people_count',
        'status', 'over_capacity', 'created_at',
    ]
    readonly_fields = ['created_at', 'over_capacity']


@admin.register(Outing)
class OutingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'booking_type', 'route', 'start_at', 'end_at',
        'instructor', 'status', 'vehicles_progress',
    ]
    list_filter = ['booking_type', 'status', 'start_at', 'route']
    list_editable = ['status', 'instructor']
    search_fields = ['route__title', 'bookings__contact_name', 'bookings__contact_phone']
    autocomplete_fields = ['route', 'instructor']
    date_hierarchy = 'start_at'
    ordering = ['-start_at']
    inlines = [BookingInline]
    readonly_fields = ['created_at', 'duration_minutes']

    @admin.display(description='Квадроциклы (набрано / минимум)')
    def vehicles_progress(self, obj):
        mark = '✓' if obj.meets_minimum else '⚠'
        return f'{obj.total_vehicles} / {obj.min_vehicles} {mark}'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'contact_name', 'contact_phone', 'outing',
        'vehicles_count', 'status', 'over_capacity', 'created_at',
    ]
    list_filter = ['status', 'over_capacity', 'created_at']
    list_editable = ['status']
    search_fields = ['contact_name', 'contact_phone', 'contact_email', 'outing__route__title']
    autocomplete_fields = ['outing']
    readonly_fields = ['created_at', 'mode_at_creation']


@admin.register(WeekendTourProgram)
class WeekendTourProgramAdmin(SingletonModelAdmin):
    pass


@admin.register(BookingSettings)
class BookingSettingsAdmin(SingletonModelAdmin):
    pass
