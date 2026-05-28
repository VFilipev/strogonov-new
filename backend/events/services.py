from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def _format_money(value):
    try:
        n = float(value or 0)
    except (TypeError, ValueError):
        n = 0
    return f"{n:,.0f}".replace(',', ' ')


def _normalize_houses(items):
    result = []
    for house in items or []:
        result.append({
            'name': house.get('name') or 'Без названия',
            'price_per_night': _format_money(house.get('price_per_night')),
            'nights': house.get('nights') or 0,
            'line_total': _format_money(house.get('line_total')),
        })
    return result


def build_event_request_email_context(instance):
    payload = instance.payload or {}
    event = payload.get('event') or {}
    contact = payload.get('contact') or {}
    accommodation = payload.get('accommodation') or {}
    groups = accommodation.get('groups') or {}
    catering = payload.get('catering') or {}
    entertainment = payload.get('entertainment') or []
    additional_services = payload.get('additional_services') or []
    pricing = payload.get('pricing_snapshot') or {}

    cottages = _normalize_houses(groups.get('cottages'))
    modular = _normalize_houses(groups.get('modular'))

    entertainment_items = [
        {
            'label': item.get('label') or item.get('id') or 'Без названия',
            'price': _format_money(item.get('price')),
        }
        for item in entertainment
    ]
    additional_items = [
        {
            'label': item.get('label') or item.get('id') or 'Без названия',
            'price': _format_money(item.get('price')),
        }
        for item in additional_services
    ]

    return {
        'request_id': instance.id,
        'created_at': instance.created_at,
        'contact_name': instance.contact_name,
        'contact_phone': instance.contact_phone or contact.get('phone') or 'Не указано',
        'contact_email': instance.contact_email or contact.get('email') or 'Не указано',
        'event_type': instance.event_type or ((event.get('type') or {}).get('title')) or 'Не указано',
        'event_date': event.get('date') or 'Не указано',
        'guest_count': event.get('guest_count') or 'Не указано',
        'check_in': accommodation.get('check_in') or 'Не указано',
        'check_out': accommodation.get('check_out') or 'Не указано',
        'nights': accommodation.get('nights') or 0,
        'cottages': cottages,
        'modular': modular,
        'accommodation_subtotal': _format_money(accommodation.get('subtotal')),
        'catering_label': catering.get('label') or 'Не выбрано',
        'catering_price_per_guest': _format_money(catering.get('price_per_guest')),
        'catering_subtotal': _format_money(catering.get('subtotal')),
        'entertainment': entertainment_items,
        'additional_services': additional_items,
        'venue_base': _format_money(pricing.get('venue_base')),
        'entertainment_subtotal': _format_money(pricing.get('entertainment_subtotal')),
        'additional_subtotal': _format_money(pricing.get('additional_subtotal')),
        'estimated_total': _format_money(pricing.get('estimated_total')),
    }


def send_event_request_email(instance):
    manager_email = getattr(settings, 'EVENT_REQUEST_MANAGER_EMAIL', '')
    if not manager_email:
        return

    context = build_event_request_email_context(instance)
    subject = (
        f"Новая заявка с калькулятора: {context['event_type']}, "
        f"{context['guest_count']} гостей"
    )
    text_body = render_to_string('events/event_request_email.txt', context)
    html_body = render_to_string('events/event_request_email.html', context)

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
        to=[manager_email],
    )
    message.attach_alternative(html_body, 'text/html')
    message.send(fail_silently=False)
