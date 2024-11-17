from django.db import models
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, verbose_name='Имя пользователя', unique=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(max_length=100, verbose_name='Email', unique=True)
    password = models.CharField(max_length=100, verbose_name='Пароль')
    password_confirm = models.CharField(max_length=100, verbose_name='Подтверждение пароля' )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')

    def __str__(self):
        return self.name

class DesignCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE,verbose_name='Создатель') # Нужен чтобы при удалении удалилось все связанное с юзером, например заявки
    title = models.CharField(max_length=200, verbose_name='Название')
    photos = models.FileField(verbose_name='Фото')
    category = models.ManyToManyField(Category,verbose_name='Категории') #Заявка может быть связана с несколькими категориями
    description = models.TextField(verbose_name='Описание')

    STATUS_CHOICES = [('N', 'Новая'), ('A','Принято'), ('С','Выполнено')]
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='new', verbose_name='Статус заявки' )

    def __str__(self):
        return self.title