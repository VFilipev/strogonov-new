import re

from rest_framework import serializers
from .models import (
    Statistic,
    GalleryImage,
    HeroSection,
    HeroImage,
    SiteSettings,
    GuestFeedback,
    AfishaEvent,
)
from .utils import get_image_url, format_afisha_event_date_label
from .serializer_mixins import ImageVariantsMixin


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ['id', 'number', 'label', 'description', 'is_active', 'order']


class GalleryImageSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    image_webp_url = serializers.SerializerMethodField()
    image_placeholder_url = serializers.SerializerMethodField()
    image_variants = serializers.SerializerMethodField()
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    column_display = serializers.CharField(source='get_column_display', read_only=True)

    class Meta:
        model = GalleryImage
        fields = [
            'id', 'image_url', 'image_webp_url', 'image_placeholder_url',
            'image_variants', 'alt_text',
            'position', 'position_display', 'column', 'column_display', 'order', 'is_active'
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_image_webp_url(self, obj):
        if not obj.image:
            return None

        request = self.context.get('request')
        try:

            if hasattr(obj, 'image_webp') and obj.image_webp:
                webp_url = obj.image_webp.url
                if request:
                    return request.build_absolute_uri(webp_url)
                return webp_url
        except Exception:

            pass


        return self.get_image_url(obj)

    def get_image_placeholder_url(self, obj):
        if not obj.image:
            return None

        request = self.context.get('request')
        try:
            placeholder_field = getattr(obj, 'gallery_placeholder_webp', None)
            if placeholder_field:
                url = placeholder_field.url
                if request:
                    url = request.build_absolute_uri(url)
                return url
        except Exception:
            pass

        return None

    def get_image_variants(self, obj):
        variant_fields = {
            'large': 'gallery_large_webp',
            'medium': 'gallery_medium_webp',
            'small': 'gallery_small_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'image')


class HeroImageSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    image_webp_url = serializers.SerializerMethodField()
    image_placeholder_url = serializers.SerializerMethodField()
    image_variants = serializers.SerializerMethodField()

    class Meta:
        model = HeroImage
        fields = [
            'id', 'image_url', 'image_webp_url', 'image_placeholder_url',
            'image_variants', 'alt_text',
            'order', 'is_active', 'transition_duration'
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_image_webp_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            try:

                webp_url = obj.hero_full_webp.url if hasattr(obj, 'hero_full_webp') and obj.hero_full_webp else None
                if not webp_url:
                    webp_url = obj.image_webp.url if hasattr(obj, 'image_webp') and obj.image_webp else None
                if webp_url:
                    if request:
                        return request.build_absolute_uri(webp_url)
                    return webp_url
            except:
                pass

            return self.get_image_url(obj)
        return None

    def get_image_placeholder_url(self, obj):
        return super().get_image_placeholder_url(obj, 'hero_placeholder_webp', 'image')

    def get_image_variants(self, obj):
        variant_fields = {
            'full': 'hero_full_webp',
            'thumb': 'hero_thumb_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'image')


class HeroSectionSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    images = HeroImageSerializer(many=True, read_only=True)
    preview_image_url = serializers.SerializerMethodField()
    preview_image_webp_url = serializers.SerializerMethodField()
    preview_image_placeholder_url = serializers.SerializerMethodField()
    preview_image_variants = serializers.SerializerMethodField()
    video_poster_url = serializers.SerializerMethodField()
    promo_video_url = serializers.SerializerMethodField()
    display_type_display = serializers.CharField(source='get_display_type_display', read_only=True)
    seo_fields = serializers.SerializerMethodField()

    class Meta:
        model = HeroSection
        fields = [
            'id', 'title', 'subtitle', 'preview_image_url', 'preview_image_webp_url',
            'preview_image_placeholder_url',
            'preview_image_variants', 'promo_video_url', 'video_poster_url',
            'display_type', 'display_type_display',
            'autoplay_video', 'loop_video', 'mute_video', 'is_active', 'order',
            'images', 'seo_fields'
        ]

    def get_preview_image_url(self, obj):
        if obj.preview_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.preview_image.url)
            return obj.preview_image.url
        return None

    def get_preview_image_webp_url(self, obj):
        if obj.preview_image:
            request = self.context.get('request')
            try:

                webp_url = obj.preview_image_hero_full_webp.url if hasattr(obj, 'preview_image_hero_full_webp') and obj.preview_image_hero_full_webp else None
                if not webp_url:
                    webp_url = obj.preview_image_webp.url if hasattr(obj, 'preview_image_webp') and obj.preview_image_webp else None
                if webp_url:
                    if request:
                        return request.build_absolute_uri(webp_url)
                    return webp_url
            except:
                pass

            return self.get_preview_image_url(obj)
        return None

    def get_preview_image_placeholder_url(self, obj):
        if not obj.preview_image:
            return None
        request = self.context.get('request')
        try:
            placeholder_field = obj.preview_image_hero_placeholder_webp if hasattr(obj, 'preview_image_hero_placeholder_webp') else None
            if placeholder_field and hasattr(placeholder_field, 'url'):
                url = placeholder_field.url
                if request:
                    url = request.build_absolute_uri(url)
                return url
        except:
            pass
        return None

    def get_preview_image_variants(self, obj):
        if not obj.preview_image:
            return None
        variant_fields = {
            'full': 'preview_image_hero_full_webp',
            'thumb': 'preview_image_hero_thumb_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'preview_image')

    def get_video_poster_url(self, obj):
        if obj.video_poster:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video_poster.url)
            return obj.video_poster.url
        return None

    def get_promo_video_url(self, obj):
        if obj.promo_video:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.promo_video.url)
            return obj.promo_video.url
        return None

    def get_seo_fields(self, obj):
        return {
            'meta_title': obj.meta_title,
            'meta_description': obj.meta_description,
            'meta_keywords': obj.meta_keywords,
            'og_title': obj.og_title,
            'og_description': obj.og_description,
            'og_image': obj.og_image.url if obj.og_image else None,
            'canonical_url': obj.canonical_url,
            'robots_meta': obj.robots_meta,
        }


class HeroSectionPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = ['title', 'subtitle', 'preview_image']


class StatisticPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ['number', 'label', 'description']


class GalleryImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'alt_text', 'position', 'column', 'order', 'is_active']
        read_only_fields = ['id']

    def validate(self, attrs):
        position = attrs.get('position', 'main')
        column = attrs.get('column')
        if position == 'main' and not column:
            raise serializers.ValidationError({
                'column': 'Для позиции "main" необходимо указать column.'
            })
        return attrs


class GalleryLayoutItemSerializer(serializers.Serializer):
    target_id = serializers.IntegerField(min_value=1)
    source_image_id = serializers.IntegerField(min_value=1, required=False, allow_null=True)
    position = serializers.ChoiceField(choices=GalleryImage.POSITION_CHOICES)
    column = serializers.ChoiceField(
        choices=GalleryImage.COLUMN_CHOICES,
        required=False,
        allow_null=True
    )
    order = serializers.IntegerField(min_value=0)
    alt_text = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)

    def validate(self, attrs):
        if attrs.get('position') == 'main' and not attrs.get('column'):
            raise serializers.ValidationError({
                'column': 'Для позиции "main" необходимо указать column.'
            })
        return attrs


class GalleryLayoutApplySerializer(serializers.Serializer):
    items = GalleryLayoutItemSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError('Список items не должен быть пустым.')

        target_ids = set()
        source_ids = set()
        active_slots = set()

        for item in items:
            target_id = item['target_id']
            source_id = item.get('source_image_id') or target_id
            slot_key = (
                item['position'],
                item.get('column'),
                item['order'],
            )

            if target_id in target_ids:
                raise serializers.ValidationError(
                    f'Дублирующийся target_id={target_id} в payload.'
                )
            target_ids.add(target_id)

            if source_id in source_ids:
                raise serializers.ValidationError(
                    f'Один и тот же source_image_id={source_id} указан несколько раз.'
                )
            source_ids.add(source_id)

            if item.get('is_active', True):
                if slot_key in active_slots:
                    raise serializers.ValidationError(
                        'Конфликт активных позиций: повторяются position/column/order.'
                    )
                active_slots.add(slot_key)

        return items


class SiteSettingsSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    national_projects_logo_url = serializers.SerializerMethodField()
    hero_image_url = serializers.SerializerMethodField()
    hero_image_variants = serializers.SerializerMethodField()
    hero_image_placeholder_url = serializers.SerializerMethodField()
    base_plan_image_url = serializers.SerializerMethodField()
    base_plan_image_variants = serializers.SerializerMethodField()
    base_plan_image_placeholder_url = serializers.SerializerMethodField()
    seo_fields = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'site_name', 'site_active', 'nav_show_services', 'nav_show_tours',
            'logo_url', 'phone_primary', 'phone_secondary',
            'email', 'address', 'telegram_url', 'vk_url',
            'registry_number', 'registry_url',
            'national_projects_logo_url', 'hero_image_url',
            'hero_image_variants', 'hero_image_placeholder_url',
            'hero_title', 'hero_subtitle',
            'base_plan_image_url', 'base_plan_image_variants',
            'base_plan_image_placeholder_url',
            'base_plan_description', 'seo_fields'
        ]

    def get_logo_url(self, obj):
        """Возвращает URL логотипа"""
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None

    def get_national_projects_logo_url(self, obj):
        if obj.national_projects_logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.national_projects_logo.url)
            return obj.national_projects_logo.url
        return None

    def get_hero_image_url(self, obj):
        if obj.hero_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_image.url)
            return obj.hero_image.url
        return None

    def get_hero_image_variants(self, obj):
        if not obj.hero_image:
            return None
        variant_fields = {
            'full': 'hero_image_full_webp',
            'thumb': 'hero_image_thumb_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'hero_image')

    def get_hero_image_placeholder_url(self, obj):
        return super().get_image_placeholder_url(obj, 'hero_image_placeholder_webp', 'hero_image')

    def get_base_plan_image_url(self, obj):

        if obj.base_plan_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.base_plan_image.url)
            return obj.base_plan_image.url
        return None

    def get_base_plan_image_variants(self, obj):
        if not obj.base_plan_image:
            return None
        variant_fields = {
            'full': 'plan_full_webp',
            'thumb': 'plan_thumb_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'base_plan_image')

    def get_base_plan_image_placeholder_url(self, obj):
        """Возвращает URL placeholder для base_plan_image"""
        return super().get_image_placeholder_url(obj, 'plan_placeholder_webp', 'base_plan_image')

    def get_seo_fields(self, obj):
        return {
            'meta_title': obj.meta_title,
            'meta_description': obj.meta_description,
            'meta_keywords': obj.meta_keywords,
            'og_title': obj.og_title,
            'og_description': obj.og_description,
            'og_image': obj.og_image.url if obj.og_image else None,
            'canonical_url': obj.canonical_url,
            'robots_meta': obj.robots_meta,
        }


MAX_FEEDBACK_ATTACHMENT_BYTES = 10 * 1024 * 1024
ALLOWED_FEEDBACK_ATTACHMENT = re.compile(
    r'\.(doc|pdf|ppt|docx|pptx|xls|xlsx|jpg|jpeg|png)$',
    re.IGNORECASE,
)


class OptionalDateField(serializers.DateField):

    def to_internal_value(self, data):
        if data in ('', None):
            return None
        return super().to_internal_value(data)


class GuestFeedbackCreateSerializer(serializers.ModelSerializer):

    visit_date = OptionalDateField(required=False, allow_null=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True, max_length=40)

    class Meta:
        model = GuestFeedback
        fields = (
            'topic',
            'name',
            'email',
            'phone',
            'visit_date',
            'visit_time',
            'message',
            'attachment',
        )

    def validate_message(self, value):
        value = (value or '').strip()
        if len(value) < 5:
            raise serializers.ValidationError('Сообщение слишком короткое.')
        return value

    def validate_attachment(self, value):
        if not value:
            return value
        if value.size > MAX_FEEDBACK_ATTACHMENT_BYTES:
            raise serializers.ValidationError('Файл больше 10 МБ.')
        name = getattr(value, 'name', '') or ''
        if not ALLOWED_FEEDBACK_ATTACHMENT.search(name):
            raise serializers.ValidationError(
                'Допустимые форматы: .doc, .pdf, .ppt, .docx, .pptx, .xls, .xlsx, .jpg, .png'
            )
        return value

    def validate(self, attrs):
        email = (attrs.get('email') or '').strip()
        phone = attrs.get('phone') or ''
        digits = re.sub(r'\D', '', phone)
        if not email and len(digits) < 10:
            raise serializers.ValidationError(
                'Укажите e-mail или телефон для обратной связи.'
            )
        return attrs


class AfishaEventSerializer(serializers.ModelSerializer):

    sortKey = serializers.SerializerMethodField()
    dateLabel = serializers.SerializerMethodField()
    shortDescription = serializers.SerializerMethodField()
    fullDescription = serializers.CharField(source='description')
    pricePerGuest = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = AfishaEvent
        fields = [
            'id',
            'sortKey',
            'dateLabel',
            'title',
            'shortDescription',
            'fullDescription',
            'pricePerGuest',
            'image',
        ]

    def get_sortKey(self, obj):
        d = obj.event_date or obj.event_date_end
        if d is None:
            return None
        return d.isoformat()

    def get_shortDescription(self, obj):
        text = (obj.short_description or '').strip()
        if text:
            return text
        return obj.description or ''

    def get_dateLabel(self, obj):
        return format_afisha_event_date_label(obj.event_date, obj.event_date_end)

    def get_pricePerGuest(self, obj):
        if obj.price_per_guest is None:
            return None
        return float(obj.price_per_guest)

    def get_image(self, obj):
        return get_image_url(obj, 'image', self.context.get('request'))


class GuestFeedbackSerializer(serializers.ModelSerializer):

    topic_display = serializers.SerializerMethodField()
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = GuestFeedback
        fields = (
            'id',
            'topic',
            'topic_display',
            'name',
            'email',
            'phone',
            'visit_date',
            'visit_time',
            'message',
            'attachment_url',
            'created_at',
        )
        read_only_fields = fields

    def get_topic_display(self, obj):
        return obj.get_topic_display()

    def get_attachment_url(self, obj):
        if not obj.attachment:
            return None
        request = self.context.get('request')
        url = obj.attachment.url
        if request:
            return request.build_absolute_uri(url)
        return url

