from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventTypeViewSet, EventCalculatorRequestViewSet

types_router = DefaultRouter()
types_router.register(r'', EventTypeViewSet, basename='eventtype')

requests_router = DefaultRouter()
requests_router.register(r'', EventCalculatorRequestViewSet, basename='eventcalculatorrequest')

urlpatterns = [
    path('types/', include(types_router.urls)),
    path('requests/', include(requests_router.urls)),
]
