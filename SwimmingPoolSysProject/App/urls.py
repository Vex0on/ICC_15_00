from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('remind_password/', views.remind_password, name='remind_password'),
]
