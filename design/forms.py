from idlelib.query import CustomRun
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
#from .models import user_registrated
from .models import CustomUser, DesignCategory
from django.core.validators import FileExtensionValidator




class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}) )
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password_confirm = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))
    email = forms.EmailField(required=True,max_length=100,widget=forms.EmailInput(attrs={'placeholder': 'Электронная почта'}))
    first_name = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs={'placeholder':'Фамилия'}))
    consent = forms.BooleanField(required=True, label='Согласие на обработку персональных данных',widget=forms.CheckboxInput())

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        user.is_active=False
        user.is_activated=False
        if commit:
            user.save()
            #user_registrated.send(CustomUser, instance=user)
        return user

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField( widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    template_name = 'registration/profile.html'

class Registration(CreateView):
      model = CustomUser  # Укажите модель
      template_name = 'registration/register.html'
      success_url = reverse_lazy('design:login')  # URL для перенаправления после успешной регистрации
      fields = ['username', 'password', 'email']  # Поля формы


class DesignCategoryForm(forms.ModelForm):
    title = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Название заявки'}))
    description = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder': 'Описание заявки' }))
    photos = forms.FileField(label="",widget=forms.FileInput(), validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp'])])

    class Meta:
        model = DesignCategory
        fields = ("photos", "category", "description", "title")

