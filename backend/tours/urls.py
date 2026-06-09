from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RouteViewSet,
    InstructorViewSet,
    WeekendTourView,
    AvailabilityView,
    WeekendAvailabilityView,
    BookingViewSet,
    ScheduleView,
)

routes_router = DefaultRouter()
routes_router.register(r'', RouteViewSet, basename='route')

instructors_router = DefaultRouter()
instructors_router.register(r'', InstructorViewSet, basename='instructor')

bookings_router = DefaultRouter()
bookings_router.register(r'', BookingViewSet, basename='booking')

urlpatterns = [
    path('weekend/', WeekendTourView.as_view(), name='tours-weekend'),
    path('availability/', AvailabilityView.as_view(), name='tours-availability'),
    path('weekend-availability/', WeekendAvailabilityView.as_view(), name='tours-weekend-availability'),
    path('schedule/', ScheduleView.as_view(), name='tours-schedule'),
    path('routes/', include(routes_router.urls)),
    path('instructors/', include(instructors_router.urls)),
    path('bookings/', include(bookings_router.urls)),
]
