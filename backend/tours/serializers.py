import re
from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import serializers

from core.serializer_mixins import ImageVariantsMixin
from .models import Booking, Instructor, Outing, Route, WeekendTourProgram
from . import services


class InstructorSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    photo_webp_url = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'role', 'bio', 'photo_url', 'photo_webp_url', 'order']

    def _abs(self, url):
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request else url

    def get_photo_url(self, obj):
        return self._abs(obj.photo.url) if obj.photo else None

    def get_photo_webp_url(self, obj):
        try:
            if obj.photo and obj.photo_webp:
                return self._abs(obj.photo_webp.url)
        except Exception:
            pass
        return None


class RouteSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    image_variants = serializers.SerializerMethodField()
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)

    class Meta:
        model = Route
        fields = [
            'id', 'title', 'slug', 'description',
            'duration_minutes', 'duration_label',
            'difficulty', 'difficulty_display',
            'min_vehicles', 'group_label', 'price',
            'photo_url', 'image_variants',
            'available_for_tour', 'tour_price', 'tour_old_price', 'tour_description',
            'tour_outing_start', 'tour_outing_end',
            'order',
        ]

    def get_photo_url(self, obj):
        if not obj.photo:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url

    def get_image_variants(self, obj):
        return super().get_image_variants(
            obj, {'large': 'route_large_webp', 'card': 'route_card_webp'}, 'photo',
        )


class WeekendTourProgramSerializer(serializers.ModelSerializer):
    routes = serializers.SerializerMethodField()

    class Meta:
        model = WeekendTourProgram
        fields = ['intro', 'benefits', 'schedule', 'included_items', 'experience_items', 'routes']

    def get_routes(self, obj):
        qs = Route.objects.filter(is_active=True, available_for_tour=True).order_by('order', 'title')
        return RouteSerializer(qs, many=True, context=self.context).data


class OutingSummarySerializer(serializers.ModelSerializer):

    total_vehicles = serializers.IntegerField(read_only=True)
    min_vehicles = serializers.IntegerField(read_only=True)
    vehicles_needed = serializers.IntegerField(read_only=True)
    meets_minimum = serializers.BooleanField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    route_title = serializers.CharField(source='route.title', read_only=True)

    class Meta:
        model = Outing
        fields = [
            'id', 'route', 'route_title', 'booking_type', 'start_at', 'end_at',
            'duration_minutes', 'checkin_date', 'status', 'status_display',
            'total_vehicles', 'min_vehicles', 'vehicles_needed', 'meets_minimum',
        ]


class BookingNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id', 'vehicles_count', 'people_count',
            'contact_name', 'contact_phone', 'contact_email',
            'status', 'over_capacity', 'created_at',
        ]


class OutingScheduleSerializer(OutingSummarySerializer):

    bookings = BookingNestedSerializer(many=True, read_only=True)
    instructor_name = serializers.CharField(source='instructor.name', read_only=True, default=None)

    class Meta(OutingSummarySerializer.Meta):
        fields = OutingSummarySerializer.Meta.fields + [
            'instructor', 'instructor_name', 'total_people', 'bookings',
        ]


class BookingCreateSerializer(serializers.ModelSerializer):

    booking_type = serializers.ChoiceField(choices=Outing.TYPE_CHOICES, default='route')
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    date = serializers.DateField(write_only=True, required=False)
    start_time = serializers.TimeField(write_only=True, required=False)
    checkin_date = serializers.DateField(write_only=True, required=False)
    join_outing = serializers.PrimaryKeyRelatedField(
        queryset=Outing.objects.all(), required=False, allow_null=True, write_only=True,
    )
    comment = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Booking
        fields = [
            'booking_type', 'route', 'date', 'start_time', 'checkin_date', 'join_outing',
            'vehicles_count', 'people_count',
            'contact_name', 'contact_phone', 'contact_email', 'comment',
        ]

    def validate_route(self, route):
        if not route.is_active:
            raise serializers.ValidationError('Маршрут недоступен.')
        return route

    def validate_contact_name(self, value):
        value = (value or '').strip()
        if len(value) < 2:
            raise serializers.ValidationError('Укажите имя (не менее 2 символов).')
        return value

    def validate_vehicles_count(self, value):
        if value < 1:
            raise serializers.ValidationError('Укажите хотя бы один квадроцикл.')
        return value

    def validate(self, attrs):
        email = (attrs.get('contact_email') or '').strip()
        digits = re.sub(r'\D', '', attrs.get('contact_phone') or '')
        if not email and len(digits) < 10:
            raise serializers.ValidationError('Укажите e-mail или телефон для связи.')

        route = attrs['route']
        booking_type = attrs.get('booking_type', 'route')
        vehicles = attrs.get('vehicles_count', 1)
        tz = timezone.get_current_timezone()

        if booking_type == 'weekend_tour':
            checkin = attrs.get('checkin_date')
            if not checkin:
                raise serializers.ValidationError({'checkin_date': 'Укажите дату заезда (пятница).'})
            if not route.available_for_tour:
                raise serializers.ValidationError({'route': 'Маршрут недоступен для тура выходного дня.'})
            window = services.weekend_outing_window(route, checkin)
            if window is None:
                raise serializers.ValidationError({'route': 'Для маршрута не задано время выезда в туре.'})
            start_at, end_at = window
        else:
            date = attrs.get('date')
            start_time = attrs.get('start_time')
            if not date or not start_time:
                raise serializers.ValidationError('Укажите дату и время выезда.')
            start_at = timezone.make_aware(datetime.combine(date, start_time), tz)
            end_at = start_at + timedelta(minutes=route.duration_minutes)

        outing = attrs.get('join_outing')
        if outing is not None:
            if outing.status in ('cancelled', 'done'):
                raise serializers.ValidationError({'join_outing': 'К этому выезду нельзя присоединиться.'})
            if outing.route_id != route.id or outing.start_at != start_at \
                    or outing.booking_type != booking_type:
                raise serializers.ValidationError({'join_outing': 'Выезд не совпадает с выбранным маршрутом/временем.'})
        else:
            outing = services.get_outing_at(route, start_at, booking_type)

        if outing is not None:
            resource_ok = services.can_join_outing(outing, vehicles)
        else:
            resource_ok = services.can_create_outing(start_at, end_at, vehicles)

        conf = services.get_settings()
        if not resource_ok and conf.booking_mode == 'strict':
            raise serializers.ValidationError(
                'На выбранное время не хватает свободного инструктора или техники. Выберите другое время.'
            )

        attrs['_start_at'] = start_at
        attrs['_end_at'] = end_at
        attrs['_outing'] = outing
        attrs['_over_capacity'] = not resource_ok
        attrs['_mode'] = conf.booking_mode
        return attrs

    def create(self, validated_data):
        start_at = validated_data.pop('_start_at')
        end_at = validated_data.pop('_end_at')
        outing = validated_data.pop('_outing')
        over_capacity = validated_data.pop('_over_capacity')
        mode = validated_data.pop('_mode')
        route = validated_data.pop('route')
        booking_type = validated_data.pop('booking_type')
        checkin = validated_data.pop('checkin_date', None)
        comment = validated_data.pop('comment', '')
        validated_data.pop('date', None)
        validated_data.pop('start_time', None)
        validated_data.pop('join_outing', None)

        if outing is None:
            outing = Outing.objects.create(
                route=route,
                booking_type=booking_type,
                start_at=start_at,
                end_at=end_at,
                duration_minutes=int((end_at - start_at).total_seconds() // 60),
                checkin_date=checkin,
                status='forming',
            )

        booking = Booking.objects.create(
            outing=outing,
            over_capacity=over_capacity,
            mode_at_creation=mode,
            payload={'comment': comment} if comment else {},
            **validated_data,
        )
        self._outing = outing
        return booking
