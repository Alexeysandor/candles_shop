from django.contrib import admin

from .models import Product, Example, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    """модель для добавления и просмотра товаров"""
    list_display = ['name', 'slug', 'description', 'price', 'available']


class ExampleAdmin(admin.ModelAdmin):
    """модель для загрузки фото примеров работ"""
    list_display = ['image']


class OrderAdmin(admin.ModelAdmin):
    """модель для просмотра заказов"""
    list_display = ('id', 'first_name', 'second_name', 'phone_number', 'email', 'address', 'postal_code', 'city', 'order_status',)
    fields = ('email', 'order_status',)


class OrderItemAdmin(admin.ModelAdmin):
    """модель для просмотра товара в заказе"""
    list_display = ['order', 'product']
    fields = ('product', 'price')


admin.site.register(Example, ExampleAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)