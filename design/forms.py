from idlelib.query import CustomRun
from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import CustomUser




class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}) )
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password_confirm = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))
    email = forms.EmailField(required=True,max_length=100,widget=forms.EmailInput(attrs={'placeholder': 'Электронная почта'}))
    first_name = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs={'placeholder':'Фамилия'}))
    consent = forms.BooleanField(required=True, label='Согласие на обработку персональных данных',widget=forms.CheckboxInput())

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email")


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField( widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    template_name = 'registration/profile.html'

class Registration(CreateView):
     model = CustomUser  # Укажите модель
     template_name = 'registration/register.html'
     success_url = reverse_lazy('login')  # URL для перенаправления после успешной регистрации
     fields = ['username', 'password', 'email']  # Поля формы

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']  # Здесь только поля, которые можно редактировать



