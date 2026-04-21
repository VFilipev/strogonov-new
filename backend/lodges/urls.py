from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LodgeTypeViewSet, LodgeViewSet, LodgeCategoryViewSet

router = DefaultRouter()
router.register(r'types', LodgeTypeViewSet, basename='lodgetype')
router.register(r'categories', LodgeCategoryViewSet, basename='lodgecategory')
router.register(r'', LodgeViewSet, basename='lodge')

urlpatterns = [
    path('', include(router.urls)),
]

