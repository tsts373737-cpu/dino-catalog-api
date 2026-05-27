from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PeriodViewSet, DietViewSet, DinosaurViewSet

router = DefaultRouter()
router.register(r'periods', PeriodViewSet, basename='period')
router.register(r'diets', DietViewSet, basename='diet')
router.register(r'dinosaurs', DinosaurViewSet, basename='dinosaur')

urlpatterns = [
    path('', include(router.urls)),
]