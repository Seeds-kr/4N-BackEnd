from django.urls import path
from . import views



urlpatterns = [
    path('folders/', views.FoldersView.as_view()),
    path('foldersupdate/',views.FolderUpdateView.as_view()),
    path('foldersdelete/', views.FolderUpdateView.as_view()),
    # path('folderlist' , views.FoldersView.as_view()),
]
