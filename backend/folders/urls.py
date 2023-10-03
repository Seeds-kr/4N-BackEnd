from django.urls import path
from . import views



urlpatterns = [
    path('folders/', views.FoldersView.as_view())
]
