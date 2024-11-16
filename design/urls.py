from bs4.diagnose import profile
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('register/', views.Registration.as_view(), name='register'),  # Регистрация
    path('login/', views.Login.as_view(), name='login'),  # Вход
    path('logout/', views.logout_view, name='logout'),  # Выход
    path('profile/', profile, name='profile'),  # Каталог
]
