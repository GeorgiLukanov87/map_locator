from django.urls import path

from map_locator.weather.views import weather

urlpatterns = (
    path('weather/', weather, name='weather'),
)
