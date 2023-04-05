from django.db import models
from django.urls import reverse
from django.utils import timezone

from users.models import CustomUser


class Product(models.Model):
    """модель товара: свечей"""
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Название товара')

    slug = models.SlugField(
        max_length=100,
        db_index=True,
        verbose_name='url товара')

    description = models.TextField(verbose_name='Описание товара')

    image = models.ImageField(upload_to='products/',
                              verbose_name='Изображение')

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена товара')

    available = models.BooleanField(default=True,
                                    verbose_name='Наличие товара')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('price',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.slug])


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Cart #{self.id}'

    def add_product(self, product, quantity=1):
        cart_item, created = self.cartitem_set.get_or_create(product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    def has_product(self, product):
        return self.cartitem_set.filter(product=product).exists()

    def remove_product(self, product):
        cart_item = self.cartitem_set.get(product=product)
        cart_item.delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'{self.id}'

    def update_quantity(self):
        self.quantity += 1
        self.save()

    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.save()
        else:
            self.delete()

    def get_total_price(self):
        return self.product.price * self.quantity


class Example(models.Model):
    """модель для загрузки фото примеров работ на главную страницу"""
    image = models.ImageField(upload_to='image_for_example/',
                              verbose_name='Изображение для примера работ')

    class Meta:
        verbose_name = 'Изображение для примера'
        verbose_name_plural = 'Изображения для примера'


class Order(models.Model):
    """модель оформления заказов"""
    CHOICES = [('Оформлен', 'Заказ оформлен'),
               ('В процессе', 'Заказ готовится'),
               ('Готов', 'Заказ готов')]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='orders',
                             verbose_name='Пользователь')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=100,
                                    verbose_name='Номер телефона')
    email = models.EmailField(max_length=45, verbose_name='Почта')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20,
                                   verbose_name='Почтовый индекс')
    city = models.CharField(max_length=100, verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата оформления')
    paid = models.BooleanField(default=False, verbose_name='Статус оплаты')
    order_status = models.CharField(default='Заказ оформлен',
                                    verbose_name='Статус заказа',
                                    choices=CHOICES,
                                    max_length=25)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_absolute_url(self):
        return reverse('shop:order_detail',
                       args=[self.id])


class OrderItem(models.Model):
    """модель товаров в заказе"""
    order = models.ForeignKey(
        Order,
        related_name='items',
        verbose_name='Заказ',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name='Предметы в заказе',
        related_name='order_items',
        on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name='Количество')

    class Meta:
        verbose_name = 'Предмет в заказе'
        verbose_name_plural = 'Предметы в заказе'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
