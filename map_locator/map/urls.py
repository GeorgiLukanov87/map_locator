from django.urls import path

from map_locator.map.views import index

urlpatterns = (
    path('', index, name='index'),
)
