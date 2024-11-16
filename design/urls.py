from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # Импортируем стандартные классы входа и выхода
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('register/', views.Registration.as_view(), name='register'),  # Регистрация
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),  # Вход
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),  # Выход
    path('profile/', views.profile, name='profile'),  # Профиль
]
