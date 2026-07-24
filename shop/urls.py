from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_login,name="login"),
    path('home/', views.home,name="home"),
    path('index/',views.index,name="index"),
    path('about/', views.about,name="AboutUs"),
    path('service/', views.Crop_recommend,name="service"),
    # path('service/', views.recommend,name="Services"),
    path('contactus/', views.user_contact ,name="contact"),
    path('signup/', views.user_signup ,name="signup"),
    path('login/', views.user_login ,name="login"),
    path('logout/', views.user_logout ,name="logout"),
    path('terms/', views.terms ,name="terms"),
    path('result/', views.result ,name="result"),
    path('history/', views.recommendation_history, name='history'),
    path('history/delete/', views.delete_history, name='delete_history'),
]
    
