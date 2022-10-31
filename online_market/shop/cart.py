from decimal import Decimal
from django.conf import settings

from .models import Product


class Cart(object):
    """класс для корзины"""
    def __init__(self, request):
        """создаём сессию и корзину внутри сессии"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            """если в сессии ещё нет корзины, создаём её"""
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add_product_to_cart(self, product, quantity=1):
        """Добавляем продукт в корзину продукт в корзину
         и задаём его количество"""
        product_id = str(product.id)
        self.cart[product_id] = {'quantity': quantity,
                                 'price': str(product.price)}
        self.save()

    def update_count_product_in_cart(self, product, quantity=1):
        """добавляем товар по 1 штуке"""
        product_id = str(product.id)
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove_product_from_cart(self, product, quantity=1):
        """удаляем товар по 1 штуке, если товара будет меньше единицы,
        полностью удаляем его из корзины"""
        product_id = str(product.id)
        self.cart[product_id]['quantity'] -= quantity
        if self.cart[product_id]['quantity'] < 1:
            del self.cart[product_id]
        self.save()

    def save(self):
        """Обновление сессии корзины"""
        self.session[settings.CART_SESSION_ID] = self.cart

    def __iter__(self):
        """функция генератор для перебора элементов в корзине"""
        product_ids = self.cart.keys()
        # получением объекты product и добавлением их в корзину
        products = Product.objects.filter(pk__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            # переводим цену в десятичное число,
            # и находим общую цену за весь товар одного типа
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
            # вместо return - yield для iter, потому это функция генератор

    def get_total_price(self):
        """подсчитываем сумму всех товаров в корзине"""
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
    # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True