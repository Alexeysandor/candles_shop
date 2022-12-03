from django.contrib import admin
from .models import Product, Example, Order


class ProductAdmin(admin.ModelAdmin):
    """регистрируем модель в админке, выводим поля"""
    list_display = ['name', 'slug', 'description', 'price', 'available']


class ExampleAdmin(admin.ModelAdmin):
    """модель для загрузки фото примеров работ"""
    list_display = ['image', ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','order_status',)
    fields = ('email','order_status',)


admin.site.register(Example, ExampleAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)