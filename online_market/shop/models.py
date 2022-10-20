from tkinter import CASCADE
from django.db import models
from django.urls import reverse


class Product(models.Model):
    """модель товара: свечей"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название товара')
    slug = models.SlugField(max_length=100, db_index=True, verbose_name='url товара')
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(upload_to='products/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
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
