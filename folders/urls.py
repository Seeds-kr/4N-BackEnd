from django.urls import path
from . import views


urlpatterns = [
    path('api/folders/', views.get_folders, name='get_folders'),
]
