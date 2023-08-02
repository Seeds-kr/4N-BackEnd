from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register ),
    path('login/', views.login),
    path('logout/', views.logout),
    path('findpassword/',views.findpassword),
    path('changepassword/',views.changepassword),
    path('findid/',views.findid),
    path('kakao/' , views.KakaoLoginView.as_view()),

]