from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from .forms import LoginForm, CustomUserCreationForm


# Главная страница
def index(request):
    return render(request, 'index.html')

# Регистрация
class Registration(generic.CreateView):
    template_name = 'registration/register.html'  # Исправлено: template_name вместо templates_name
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Переход после успешной регистрации, например, на страницу входа

# Вход
class Login(View):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def get(self, request):
        form = LoginForm()
        next_page = request.GET.get('next', '')  # Получаем next из GET параметров
        return render(request, self.template_name, {'form': form, 'next': next_page})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_page = request.POST.get('next') or reverse_lazy('design:index')  # Получаем next из POST данных
                return redirect(next_page)
            else:
                form.add_error(None, 'Неверные учетные данные.')

        return render(request, self.template_name, {'form': form})

# Выход
def logout_view(request):
    logout(request)  # Выход пользователя
    return render(request, 'registration/logout.html')

# Профиль
@login_required
def profile(request):
    # Получаем текущего пользователя
    user = request.user

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('registration:profile'))  # Перенаправление на профиль после успешного сохранения
    else:
        form = CustomUserCreationForm(instance=user)  # Инициализация формы с данными пользователя

    return render(request, 'registration/profile.html', {'form': form})