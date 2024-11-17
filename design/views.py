from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from .forms import LoginForm, CustomUserCreationForm, DesignCategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import DesignCategory


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
    #form_class = LoginForm

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

class DesignRequestCreateView(LoginRequiredMixin, generic.CreateView):
    model = DesignCategory
    form_class =  DesignCategoryForm
    template_name = 'registration/design_request_create.html'
    success_url = '/registration/profile/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CreatingAppProfileView(LoginRequiredMixin, generic.ListView):
    model = DesignCategory
    template_name = 'registration/design_request_list.html'
    context_object_name = 'design_requests'
    success_url = '/registration/profile/'

    def get_queryset(self):
        return DesignCategory.objects.filter(user=self.request.user) # Нужно чтобы пользователь видел только свои заявки, а не с базы данных