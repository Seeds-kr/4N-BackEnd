from django.urls import path
from . import views


urlpatterns = [
    path('api/get_location_preview/', views.get_location_preview, name='get_location_preview'),
]
