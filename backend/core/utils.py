"""
Утилиты для работы с изображениями и WebP
"""
from django.core.files.images import get_image_dimensions


_MONTHS_GENITIVE_RU = (
    '',
    'января',
    'февраля',
    'марта',
    'апреля',
    'мая',
    'июня',
    'июля',
    'августа',
    'сентября',
    'октября',
    'ноября',
    'декабря',
)


def format_afisha_date_label(d):
    if d is None:
        return None
    return f'{d.day} {_MONTHS_GENITIVE_RU[d.month]}'


def format_afisha_event_date_label(start, end):
    if start is None and end is None:
        return None
    if start is None:
        return format_afisha_date_label(end)
    if end is None or end == start:
        return format_afisha_date_label(start)
    if end < start:
        start, end = end, start
    if start.year == end.year and start.month == end.month:
        if start.day == end.day:
            return format_afisha_date_label(start)
        return f'{start.day}-{end.day} {_MONTHS_GENITIVE_RU[start.month]}'
    left = f'{start.day} {_MONTHS_GENITIVE_RU[start.month]}'
    right = f'{end.day} {_MONTHS_GENITIVE_RU[end.month]}'
    if start.year != end.year:
        left = f'{left} {start.year} г.'
        right = f'{right} {end.year} г.'
    return f'{left} – {right}'


def get_webp_url(obj, field_name='image_webp', fallback_field='image', request=None):

    original_image = getattr(obj, fallback_field, None)
    if not original_image:
        return None

    try:
        webp_field = getattr(obj, field_name, None)
        if webp_field and hasattr(webp_field, 'url'):
            webp_url = webp_field.url
            if request:
                return request.build_absolute_uri(webp_url)
            return webp_url
    except (AttributeError, ValueError, Exception):
        pass


    try:
        original_url = original_image.url
        if request:
            return request.build_absolute_uri(original_url)
        return original_url
    except (AttributeError, ValueError, Exception):
        return None


def get_image_url(obj, field_name='image', request=None):
    image = getattr(obj, field_name, None)
    if not image:
        return None

    try:
        image_url = image.url
        if request:
            return request.build_absolute_uri(image_url)
        return image_url
    except (AttributeError, ValueError, Exception):
        return None

