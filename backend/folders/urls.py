from django.urls import path
from . import views



urlpatterns = [
    path('folders/', views.FoldersView.as_view()),
    path('foldersupdate/<int:folder_id>',views.FolderUpdateView.as_view()),
    path('foldersdel/<int:folder_id>', views.FolderUpdateView.as_view()),
    path('folderlist', views.FolderListView.as_view()),
]
