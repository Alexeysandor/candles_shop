from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff']



admin.site.register(CustomUser, CustomUserAdmin)
# Register your models here.
