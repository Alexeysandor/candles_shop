from django.db import models
from django.urls import reverse


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
    image = models.ImageField(upload_to='products/', blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена товара')
    available = models.BooleanField(default=True, verbose_name='Наличие товара')

    class Meta:
        """индексируем поля id и slug вместе чтобы упростить запросы"""
        ordering = ('price',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.slug])


class Example(models.Model):
    """модель для загрузки фото примеров работ на главную страницу"""
    image = models.ImageField(upload_to='image_for_example/')


class Order(models.Model):
    CHOICES = [('Оформлен', 'Заказ оформлен'),
               ('В процессе', 'Заказ готовится'),
               ('Готов', 'Заказ готов')]
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    order_status = models.CharField(
        default='Заказ оформлен',
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
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
