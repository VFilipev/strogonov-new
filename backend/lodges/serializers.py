from rest_framework import serializers
from .models import LodgeType, Lodge, LodgeImage, LodgePrice, LodgeAvailability, LodgeCategory
from core.serializer_mixins import ImageVariantsMixin


class LodgeImageSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    image_webp_url = serializers.SerializerMethodField()
    image_placeholder_url = serializers.SerializerMethodField()
    image_variants = serializers.SerializerMethodField()

    class Meta:
        model = LodgeImage
        fields = [
            'id', 'image_url', 'image_webp_url', 'image_placeholder_url',
            'image_variants', 'alt_text', 'order'
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

                webp_url = obj.lodge_main_webp.url if hasattr(obj, 'lodge_main_webp') and obj.lodge_main_webp else None
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
        return super().get_image_placeholder_url(obj, 'lodge_placeholder_webp', 'image')

    def get_image_variants(self, obj):
        variant_fields = {
            'main': 'lodge_main_webp',
            'card': 'lodge_card_webp',
            'thumb': 'lodge_thumb_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'image')


class LodgePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LodgePrice
        fields = ['id', 'name', 'cost', 'order']


class LodgeAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LodgeAvailability
        fields = ['id', 'name', 'order']


class LodgeSerializer(serializers.ModelSerializer):
    images = LodgeImageSerializer(many=True, read_only=True)
    lodge_type_name = serializers.CharField(source='lodge_type.name', read_only=True)
    lodge_type_slug = serializers.CharField(source='lodge_type.slug', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    price_set = LodgePriceSerializer(many=True, read_only=True)
    special_price_set = serializers.SerializerMethodField()
    availability_set = LodgeAvailabilitySerializer(many=True, read_only=True)
    schema_org_json = serializers.SerializerMethodField()
    seo_fields = serializers.SerializerMethodField()

    class Meta:
        model = Lodge
        fields = [
            'id', 'name', 'slug', 'lodge_type', 'lodge_type_name', 'lodge_type_slug',
            'category_id', 'category_name', 'category_slug',
            'description', 'short_description', 'capacity', 'area', 'price_from',
            'location_description', 'is_active', 'order', 'conveniences', 'include',
            'bronirui_online_url',
            'images', 'price_set', 'special_price_set', 'availability_set',
            'schema_org_json', 'seo_fields'
        ]

    def get_special_price_set(self, obj):
        return []

    def get_schema_org_json(self, obj):
        return obj.get_schema_org_json()

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


class LodgeCategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    capacity_max = serializers.SerializerMethodField()
    price_from_min = serializers.SerializerMethodField()

    class Meta:
        model = LodgeCategory
        fields = [
            'id', 'lodge_type', 'name', 'slug', 'description', 'image_url',
            'capacity_max', 'price_from_min', 'is_active', 'order'
        ]

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    def get_capacity_max(self, obj):
        return obj.get_capacity_max()

    def get_price_from_min(self, obj):
        return obj.get_price_from_min()


class LodgeTypeListSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    hero_image_url = serializers.SerializerMethodField()
    hero_image_webp_url = serializers.SerializerMethodField()
    hero_image_placeholder_url = serializers.SerializerMethodField()
    hero_image_variants = serializers.SerializerMethodField()

    class Meta:
        model = LodgeType
        fields = [
            'id', 'name', 'slug', 'subtitle', 'hero_image_url',
            'hero_image_webp_url', 'hero_image_placeholder_url',
            'hero_image_variants', 'description', 'is_active', 'order'
        ]

    def get_hero_image_url(self, obj):
        if obj.hero_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_image.url)
            return obj.hero_image.url
        return None

    def get_hero_image_webp_url(self, obj):
        if obj.hero_image:
            request = self.context.get('request')
            try:
                webp_url = obj.lodge_hero_main_webp.url if hasattr(obj, 'lodge_hero_main_webp') and obj.lodge_hero_main_webp else None
                if not webp_url:
                    webp_url = obj.hero_image_webp.url if hasattr(obj, 'hero_image_webp') and obj.hero_image_webp else None
                if webp_url:
                    if request:
                        return request.build_absolute_uri(webp_url)
                    return webp_url
            except:
                pass
            return self.get_hero_image_url(obj)
        return None

    def get_hero_image_placeholder_url(self, obj):
        return super().get_image_placeholder_url(obj, 'lodge_hero_placeholder_webp', 'hero_image')

    def get_hero_image_variants(self, obj):
        if not obj.hero_image:
            return None
        variant_fields = {
            'main': 'lodge_hero_main_webp',
            'card': 'lodge_hero_card_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'hero_image')


class LodgeTypeSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    lodges = LodgeSerializer(many=True, read_only=True)
    categories = serializers.SerializerMethodField()
    hero_image_url = serializers.SerializerMethodField()
    hero_image_webp_url = serializers.SerializerMethodField()
    hero_image_placeholder_url = serializers.SerializerMethodField()
    hero_image_variants = serializers.SerializerMethodField()
    seo_fields = serializers.SerializerMethodField()

    class Meta:
        model = LodgeType
        fields = [
            'id', 'name', 'slug', 'subtitle', 'hero_image_url', 'hero_image_webp_url',
            'hero_image_placeholder_url',
            'hero_image_variants', 'description', 'is_active', 'order',
            'lodges', 'categories', 'seo_fields'
        ]

    def get_hero_image_url(self, obj):
        if obj.hero_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_image.url)
            return obj.hero_image.url
        return None

    def get_hero_image_webp_url(self, obj):
        if obj.hero_image:
            request = self.context.get('request')
            try:

                webp_url = obj.lodge_hero_main_webp.url if hasattr(obj, 'lodge_hero_main_webp') and obj.lodge_hero_main_webp else None
                if not webp_url:
                    webp_url = obj.hero_image_webp.url if hasattr(obj, 'hero_image_webp') and obj.hero_image_webp else None
                if webp_url:
                    if request:
                        return request.build_absolute_uri(webp_url)
                    return webp_url
            except:
                pass

            return self.get_hero_image_url(obj)
        return None

    def get_hero_image_placeholder_url(self, obj):
        return super().get_image_placeholder_url(obj, 'lodge_hero_placeholder_webp', 'hero_image')

    def get_hero_image_variants(self, obj):
        if not obj.hero_image:
            return None
        variant_fields = {
            'main': 'lodge_hero_main_webp',
            'card': 'lodge_hero_card_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'hero_image')

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

    def get_categories(self, obj):
        categories = getattr(obj, 'active_categories', None)
        if categories is None:
            categories = LodgeCategory.objects.filter(
                lodge_type=obj,
                is_active=True
            ).order_by('order', 'name')
        return LodgeCategorySerializer(categories, many=True, context=self.context).data

