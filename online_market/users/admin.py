from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name',
                    'phone_number', 'address', 'postal_code',
                    'city', 'orders_count']


admin.site.register(CustomUser, CustomUserAdmin)
