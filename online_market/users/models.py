from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """модель пользователя"""
    username = models.CharField(max_length=50, default='', unique=True,
                                verbose_name='Логин')
    email = models.EmailField(unique=True,
                              verbose_name='Адрес электронной почты')
    first_name = models.CharField(max_length=50, default='',
                                  verbose_name='Имя')
    second_name = models.CharField(max_length=50, default='',
                                   verbose_name='Фамилия')
    phone_number = models.CharField(max_length=15, default='')
    address = models.CharField(max_length=250, default='')
    postal_code = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=100, default='')
    orders_count = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    register_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        index_together = (('id', 'username'),)

    def get_absolute_url(self):
        return reverse('users:profile',
                       args=[self.username])

    def __str__(self):
        return self.email
