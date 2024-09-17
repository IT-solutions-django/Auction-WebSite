from django.urls import path, include
from .views import CarViewSet
from rest_framework.routers import DefaultRouter


api_router = DefaultRouter()
api_router.register('cars',CarViewSet,basename='cars')




urlpatterns = [
    path('',include(api_router.urls)),
]