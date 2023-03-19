from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    """модель пользователя"""
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=15, default='')
    address = models.CharField(max_length=250, default='')
    postal_code = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=100, default='')
    orders_count = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        index_together = (('id', 'username'),)

    def get_absolute_url(self):
        return reverse('users:profile',
                       args=[self.username])

    def __str__(self):
        return self.email
