from datetime import date as date_cls, datetime

from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Instructor, Outing, Route, WeekendTourProgram
from .serializers import (
    BookingCreateSerializer,
    InstructorSerializer,
    OutingScheduleSerializer,
    OutingSummarySerializer,
    RouteSerializer,
    WeekendTourProgramSerializer,
)
from . import services


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.filter(is_active=True)
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    ordering = ['order', 'title']

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


class InstructorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instructor.objects.filter(is_active=True)
    serializer_class = InstructorSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


class WeekendTourView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        program = WeekendTourProgram.get_solo()
        return Response(WeekendTourProgramSerializer(program, context={'request': request}).data)


def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


class AvailabilityView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        route_id = request.query_params.get('route')
        date = _parse_date(request.query_params.get('date'))
        if not route_id or not date:
            return Response(
                {'detail': 'Параметры route и date (YYYY-MM-DD) обязательны.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            route = Route.objects.get(pk=route_id, is_active=True)
        except Route.DoesNotExist:
            return Response({'detail': 'Маршрут не найден.'}, status=status.HTTP_404_NOT_FOUND)

        starts = services.available_start_times(route, date)
        forming = services.forming_outings(route, date)
        conf = services.get_settings()
        return Response({
            'route': route.id,
            'date': date.isoformat(),
            'mode': conf.booking_mode,
            'instructor_capacity': services.instructor_count(),
            'fleet_size': services.fleet_size(),
            'duration_minutes': route.duration_minutes,
            'min_vehicles': route.min_vehicles,
            'has_slots': bool(starts),
            'slots': [dt.isoformat() for dt in starts],
            'forming_outings': OutingSummarySerializer(forming, many=True, context={'request': request}).data,
        })


class WeekendAvailabilityView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        route_id = request.query_params.get('route')
        checkin = _parse_date(request.query_params.get('checkin_date'))
        if not route_id or not checkin:
            return Response(
                {'detail': 'Параметры route и checkin_date (YYYY-MM-DD) обязательны.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            route = Route.objects.get(pk=route_id, is_active=True, available_for_tour=True)
        except Route.DoesNotExist:
            return Response({'detail': 'Маршрут недоступен для тура.'}, status=status.HTTP_404_NOT_FOUND)

        window = services.weekend_outing_window(route, checkin)
        if window is None:
            return Response({'detail': 'Для маршрута не задано время выезда в туре.'},
                            status=status.HTTP_400_BAD_REQUEST)
        start_at, end_at = window
        existing = services.get_outing_at(route, start_at, 'weekend_tour')
        conf = services.get_settings()
        if existing is not None:
            resource_ok = services.can_join_outing(existing, 1)
        else:
            resource_ok = services.can_create_outing(start_at, end_at, 1)
        return Response({
            'route': route.id,
            'checkin_date': checkin.isoformat(),
            'outing_start': start_at.isoformat(),
            'outing_end': end_at.isoformat(),
            'mode': conf.booking_mode,
            'min_vehicles': route.min_vehicles,
            'available': resource_ok,
            'can_request': resource_ok or conf.booking_mode == 'lite',
            'existing_outing': OutingSummarySerializer(existing, context={'request': request}).data
            if existing else None,
        })


class BookingViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Outing.objects.none()
    parser_classes = [JSONParser]

    def get_serializer_class(self):
        return BookingCreateSerializer

    def get_permissions(self):
        return [AllowAny()]

    def get_authenticators(self):
        return []

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            booking = serializer.save()
            services.send_tour_request_email(booking)

        outing = booking.outing
        guaranteed = outing.meets_minimum
        if guaranteed:
            message = 'Заявка принята, мы свяжемся с вами для подтверждения.'
        else:
            message = (
                f'Заявка принята. Сейчас в группе {outing.total_vehicles} из '
                f'{outing.min_vehicles} квадроциклов — проведение пока не гарантируется, '
                f'выезд состоится при наборе группы. Мы свяжемся с вами.'
            )
        if booking.over_capacity:
            message += ' Свободного места по технике/инструктору на это время не было — заявка в листе ожидания.'

        return Response({
            'booking_id': booking.id,
            'guaranteed': guaranteed,
            'over_capacity': booking.over_capacity,
            'message': message,
            'outing': OutingSummarySerializer(outing, context={'request': request}).data,
        }, status=status.HTTP_201_CREATED)


class ScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from = _parse_date(request.query_params.get('date_from')) or date_cls.today()
        date_to = _parse_date(request.query_params.get('date_to')) or date_from

        grid = services.schedule_grid(date_from, date_to)
        return Response({
            'date_from': date_from.isoformat(),
            'date_to': date_to.isoformat(),
            'instructor_capacity': grid['instructor_capacity'],
            'fleet_size': grid['fleet_size'],
            'work_day_start': grid['work_day_start'],
            'work_day_end': grid['work_day_end'],
            'slot_step_minutes': grid['slot_step_minutes'],
            'outings': OutingScheduleSerializer(
                grid['outings'], many=True, context={'request': request}
            ).data,
        })
