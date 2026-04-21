from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django.db.models import Max, Min, Prefetch, Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import LodgeType, Lodge, LodgeCategory
from .serializers import LodgeTypeSerializer, LodgeSerializer, LodgeCategorySerializer, LodgeTypeListSerializer
from .filters import LodgeFilter


class LodgeTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LodgeTypeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']

    def _is_compact_mode(self):
        value = str(self.request.query_params.get('compact', '')).lower()
        return value in {'1', 'true', 'yes'}

    def get_queryset(self):
        queryset = LodgeType.objects.filter(is_active=True)
        if self._is_compact_mode():
            return queryset
        return queryset.prefetch_related(
            Prefetch(
                'categories',
                queryset=LodgeCategory.objects.filter(is_active=True).annotate(
                    capacity_max=Max('lodges__capacity', filter=Q(lodges__is_active=True)),
                    price_from_min=Min('lodges__price_from', filter=Q(lodges__is_active=True)),
                ).order_by('order', 'name'),
                to_attr='active_categories'
            ),
            Prefetch(
                'lodges',
                queryset=Lodge.objects.filter(is_active=True).select_related('lodge_type', 'category').prefetch_related(
                    'images', 'price_set', 'availability_set'
                )
            )
        )

    def get_serializer_class(self):
        if self._is_compact_mode():
            return LodgeTypeListSerializer
        return LodgeTypeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LodgeCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LodgeCategory.objects.filter(is_active=True).select_related('lodge_type').annotate(
        capacity_max=Max('lodges__capacity', filter=Q(lodges__is_active=True)),
        price_from_min=Min('lodges__price_from', filter=Q(lodges__is_active=True)),
    )
    serializer_class = LodgeCategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['lodge_type', 'is_active']
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LodgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lodge.objects.filter(is_active=True).select_related('lodge_type', 'category').prefetch_related(
        'images', 'price_set', 'availability_set'
    )
    serializer_class = LodgeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = LodgeFilter
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['order', 'name', 'price_from', 'capacity']
    ordering = ['order', 'name']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
