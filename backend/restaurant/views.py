from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Restaurant, RestaurantImage, MealType, RestaurantBenefit
from .serializers import (
    RestaurantSerializer, RestaurantImageSerializer,
    MealTypeSerializer, RestaurantBenefitSerializer
)


class RestaurantView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return Restaurant.objects.get()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RestaurantImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RestaurantImage.objects.all()
    serializer_class = RestaurantImageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['restaurant']
    ordering_fields = ['order']
    ordering = ['order']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class MealTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MealType.objects.all()
    serializer_class = MealTypeSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']


class RestaurantBenefitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RestaurantBenefit.objects.all()
    serializer_class = RestaurantBenefitSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['restaurant']
    ordering_fields = ['order']
    ordering = ['order']
