from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q, Sum
from django.template.loader import render_to_string
from django.utils import timezone

from .models import BookingSettings, Outing


def get_settings():
    return BookingSettings.get_solo()


def instructor_count():
    return get_settings().get_instructor_count()


def fleet_size():
    return get_settings().quad_fleet_size


def _aware(date, time):
    return timezone.make_aware(datetime.combine(date, time), timezone.get_current_timezone())


def _sweep_peak(intervals):
    points = []
    for start, end, weight in intervals:
        if start >= end:
            continue
        points.append((start, weight))
        points.append((end, -weight))
    points.sort(key=lambda p: (p[0], p[1]))
    current = peak = 0
    for _, delta in points:
        current += delta
        peak = max(peak, current)
    return peak


def _overlapping_outings(start_at, end_at, exclude_id=None):
    qs = Outing.objects.active().overlapping(start_at, end_at).annotate(
        veh=Sum('bookings__vehicles_count', filter=~Q(bookings__status='cancelled'))
    )
    if exclude_id is not None:
        qs = qs.exclude(pk=exclude_id)
    return qs


def peak_outing_count(start_at, end_at, exclude_id=None):
    intervals = [
        (max(o.start_at, start_at), min(o.end_at, end_at), 1)
        for o in _overlapping_outings(start_at, end_at, exclude_id)
    ]
    return _sweep_peak(intervals)


def peak_quads(start_at, end_at, exclude_id=None):
    intervals = [
        (max(o.start_at, start_at), min(o.end_at, end_at), o.veh or 0)
        for o in _overlapping_outings(start_at, end_at, exclude_id)
    ]
    return _sweep_peak(intervals)


def instructor_free(start_at, end_at, exclude_id=None):
    cap = instructor_count()
    if cap <= 0:
        return False
    return peak_outing_count(start_at, end_at, exclude_id) < cap


def quads_free(start_at, end_at, vehicles, exclude_id=None):
    fleet = fleet_size()
    if fleet <= 0:
        return True
    return peak_quads(start_at, end_at, exclude_id) + vehicles <= fleet


def can_create_outing(start_at, end_at, vehicles):
    return instructor_free(start_at, end_at) and quads_free(start_at, end_at, vehicles)


def can_join_outing(outing, vehicles):
    fleet = fleet_size()
    if fleet <= 0:
        return True
    return peak_quads(outing.start_at, outing.end_at) + vehicles <= fleet


def get_outing_at(route, start_at, booking_type):
    return (
        Outing.objects.active()
        .filter(route=route, start_at=start_at, booking_type=booking_type)
        .first()
    )


def available_start_times(route, date):
    conf = get_settings()
    if instructor_count() <= 0:
        return []
    duration = timedelta(minutes=route.duration_minutes)
    step = timedelta(minutes=conf.slot_step_minutes or 30)
    day_start = _aware(date, conf.work_day_start)
    day_end = _aware(date, conf.work_day_end)

    results = []
    cursor = day_start
    while cursor + duration <= day_end:
        if can_create_outing(cursor, cursor + duration, 1):
            results.append(cursor)
        cursor += step
    return results


def forming_outings(route, date):
    day_start = _aware(date, get_settings().work_day_start)
    day_end = _aware(date, get_settings().work_day_end)
    outings = (
        Outing.objects.active()
        .filter(route=route, start_at__gte=day_start, start_at__lt=day_end)
        .filter(status__in=['forming', 'confirmed'])
        .order_by('start_at')
    )
    return [o for o in outings if can_join_outing(o, 1)]


def weekend_outing_window(route, checkin_date):
    if not route.tour_outing_start or not route.tour_outing_end:
        return None
    outing_date = checkin_date + timedelta(days=1)
    return _aware(outing_date, route.tour_outing_start), _aware(outing_date, route.tour_outing_end)


def schedule_grid(date_from, date_to):
    conf = get_settings()
    range_start = _aware(date_from, conf.work_day_start)
    range_end = _aware(date_to, conf.work_day_end) + timedelta(days=1)
    outings = (
        Outing.objects.active()
        .filter(start_at__lt=range_end, end_at__gt=range_start)
        .select_related('route', 'instructor')
        .prefetch_related('bookings')
        .order_by('start_at')
    )
    return {
        'instructor_capacity': instructor_count(),
        'fleet_size': fleet_size(),
        'work_day_start': conf.work_day_start,
        'work_day_end': conf.work_day_end,
        'slot_step_minutes': conf.slot_step_minutes,
        'outings': outings,
    }


def send_tour_request_email(booking):
    manager_email = getattr(settings, 'TOUR_REQUEST_MANAGER_EMAIL', '') or getattr(
        settings, 'EVENT_REQUEST_MANAGER_EMAIL', ''
    )
    if not manager_email:
        return

    outing = booking.outing
    context = {
        'booking': booking,
        'type_label': outing.get_booking_type_display(),
        'route_title': outing.route.title,
        'start_at': outing.start_at,
        'end_at': outing.end_at,
        'checkin_date': outing.checkin_date,
        'contact_name': booking.contact_name,
        'contact_phone': booking.contact_phone or 'Не указано',
        'contact_email': booking.contact_email or 'Не указано',
        'vehicles_count': booking.vehicles_count,
        'people_count': booking.people_count or 'Не указано',
        'total_vehicles': outing.total_vehicles,
        'min_vehicles': outing.min_vehicles,
        'meets_minimum': outing.meets_minimum,
        'vehicles_needed': outing.vehicles_needed,
        'over_capacity': booking.over_capacity,
        'mode': booking.mode_at_creation,
    }
    subject = f"Новая заявка на тур: {outing.route.title} ({outing.start_at:%d.%m.%Y %H:%M})"
    text_body = render_to_string('tours/tour_request_email.txt', context)
    html_body = render_to_string('tours/tour_request_email.html', context)

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
        to=[manager_email],
    )
    message.attach_alternative(html_body, 'text/html')
    message.send(fail_silently=True)
