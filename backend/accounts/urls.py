from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('findpassword/', views.findpassword),
    path('changepassword/', views.changepassword),
    path('findid/', views.findid),
    path('del/', views.delete),
    path('kakaologin/', views.KakaoLoginView.as_view()),
    path('kakaologout/', views.KakaoLogoutView.as_view()),
    path('kakaodel/', views.KakaoUnLinkView.as_view()),
    path('naverlogin/', views.NaverLoginView.as_view()),
    path('naverlogout/', views.NaverLogoutView.as_view()),
    path('naverdel/', views.NaverUnLinkView.as_view()),
]