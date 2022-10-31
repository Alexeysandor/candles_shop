

import email
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from .cart import Cart
from .forms import CartAddProductForm, OrderForm
from .models import Example, Order, Product, OrderItem
from .utils import paginator



def index(request):
    """функция представления главной страницы"""
    # выгружае товар, который в наличии
    product = Product.objects.filter(available=True)
    # выгружаем фото примеров с использованием модели
    image_for_example = Example.objects.all()
    return render(request, 'shop/index.html', {'product': product,
                                               'image_for_example':
                                               image_for_example})


def product_detail(request, slug):
    """функция представления для страницы с конкретным товаром"""
    cart_product_form = CartAddProductForm()
    product_id = get_object_or_404(Product,
                                   slug=slug,
                                   available=True)
    if cache.get(product_id):
        product = cache.get(product_id)
    else:
        product = product_id
        cache.set(
            product_id, product, 60
        )
    return render(request,
                  'shop/product_detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})



def catalog(request):
    """функция представления для каталого товаров"""
    # выгружаем все продукты и подключаем паджинатор
    product_list = Product.objects.all()
    page_number = request.GET.get('page')
    product = paginator(product_list,
                        settings.PRODUCT_COUNT).get_page(page_number)
    return render(request, 'shop/catalog.html', {'product': product})


@cache_page(60*60)
def about_us(request):
    """функция представления для страницы 'О нас'"""
    return render(request, 'shop/about_us.html',)


def cart_detail(request):
    """функция представления для корзины"""
    cart = Cart(request)
    request.session.set_expiry(60)
    return render(request, 'shop/cart.html', {'cart': cart})


def cart_add(request, product_id):
    """функция представления для добавления товара в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.add_product_to_cart(product=product,
                                 quantity=form.cleaned_data['quantity'])
        return redirect('shop:cart_detail')


def cart_update(request, product_id):
    """функция представления для увеличения количества товара в корзине"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.update_count_product_in_cart(product)
    return redirect('shop:cart_detail')


def cart_remove(request, product_id):
    """функция представления для уменьшения количества товара в корзине
     и его удаления, если значение будет меньше единицы"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_product_from_cart(product)
    return redirect('shop:cart_detail')


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order = order, 
                                         product = item['product'], 
                                         price = item['price'], 
                                         quantity = item['quantity'])
            cart.clear()
            return render(request, 'shop/order_created.html', {'order': order})
    else:
        form = OrderForm
    return render(request, 'shop/order_create.html',
                  {'cart': cart, 'form': form})


def order_list(request):
    order = Order.objects.get(email= request.user.email)
    order_item = OrderItem.objects.get(order=order)
    return render(request, 'shop/order_list.html', {'order': order,
                                                    'order_item': order_item})
                