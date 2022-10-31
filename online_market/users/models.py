from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, default='')
    first_name = models.CharField(max_length=50, db_index=True, default='')
    second_name = models.CharField(max_length=50, db_index=True, default='')
    patronymic = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, default='')
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    register_date = models.DateTimeField(default=timezone.now)
    orders_count = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    object = CustomUserManager()

    class Meta:
        index_together = (('id', 'username'),)

    def get_absolute_url(self):
        return reverse('users:profile',
                       args=[self.username])

    def __str__(self):
        return self.email
