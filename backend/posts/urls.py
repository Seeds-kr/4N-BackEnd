from django.urls import path
from . import views


urlpatterns = [
    path('postcreate/', views.PostListView.as_view()),
    path('postlist/', views.PostListView.as_view()),
    path('postupdate/<int:post_id>', views.PostDetailView.as_view(), name='postupdate'),
    path('postdel/<int:post_id>', views.PostDetailView.as_view(), name='postdel'),
]