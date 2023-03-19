from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)
from django.views.generic.base import TemplateView

from shop.forms import CartAddProductForm, OrderForm
from shop.models import Cart, CartItem, Example, Order, OrderItem, Product
from users.models import CustomUser


@method_decorator(cache_page(60), name='dispatch')
class IndexView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'image_for_example'
    queryset = Example.objects.all()


@method_decorator(cache_page(60), name='dispatch')
class CatalogView(ListView):
    template_name = 'shop/catalog.html'
    context_object_name = 'product'
    queryset = Product.objects.all()
    paginate_by = settings.PRODUCT_COUNT


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    queryset = Product.objects.all()

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(self.queryset, slug=slug, available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = Cart.objects.get(user=self.request.user)
            context['product_in_cart'] = cart.has_product(self.get_object())
        context['cart_product_form'] = CartAddProductForm()
        return context


@method_decorator(cache_page(60*60), name='dispatch')
class AboutUsView(TemplateView):
    template_name = 'shop/about_us.html'


class CartView(LoginRequiredMixin, ListView):
    template_name = 'shop/cart.html'
    paginate_by = settings.PRODUCT_COUNT

    def get_queryset(self):
        try:
            cart = Cart.objects.prefetch_related(
                'cartitem_set__product').get(user=self.request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=self.request.user)
        return CartItem.objects.filter(cart=cart).order_by('product__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_price = sum(item.get_total_price() for item in cart_items)
        paginator = Paginator(cart_items, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['total_price'] = total_price
        context['cart_items'] = page_obj
        return context


class AddProductToCartView(CreateView):
    model = CartItem
    fields = ['quantity']
    success_url = reverse_lazy('shop:cart_detail')

    def form_valid(self, form):
        cart = Cart.objects.get(user=self.request.user)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        form.instance.cart = cart
        form.instance.product = product
        return super().form_valid(form)


class CartProductQuantityUpdateView(UpdateView):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        item_cart = CartItem.objects.get(product_id=product_id)
        item_cart.update_quantity()
        return redirect('shop:cart_detail')


class CartProductQuantityDecreaseView(UpdateView):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        item_cart = CartItem.objects.get(product_id=product_id)
        item_cart.decrease_quantity()
        return redirect('shop:cart_detail')


class ClearCartView(LoginRequiredMixin, DeleteView):
    model = Cart
    template_name = 'shop/cart.html'

    def get_object(self, queryset=None):
        return Cart.objects.get(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        cart = self.get_object()
        cart.cartitem_set.all().delete()
        return self.get(request, *args, **kwargs)


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'shop/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('shop:order_created')

    def get_initial(self):
        initial_dict = {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'phone_number': self.request.user.phone_number,
            'city': self.request.user.city,
            'address': self.request.user.address,
            'postal_code': self.request.user.postal_code
        }
        return initial_dict

    def get_queryset(self):
        cart_items = CartItem.objects.select_related(
            'product').prefetch_related(
            'cart').filter(cart__user=self.request.user)
        return cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_price = sum(item.get_total_price() for item in cart_items)
        context['total_price'] = total_price
        context['item_in_order'] = cart_items
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.email = self.request.user.email
        order.save()
        cart_items = self.get_queryset()
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity)
        cart_items.delete()
        orders = self.request.user.orders_count + 1
        CustomUser.objects.filter(
            email=self.request.user.email).update(orders_count=orders)
        return super().form_valid(form)


@method_decorator(cache_page(60*60), name='dispatch')
class OrderCreatedView(LoginRequiredMixin, TemplateView):
    template_name = 'shop/order_created.html'


class OrderDetailView(DetailView):
    model = OrderItem
    template_name = 'shop/order_detail.html'
    queryset = OrderItem.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect(reverse('shop:catalog'))
        current_order = self.get_object()
        if current_order.user != self.request.user:
            return redirect(reverse('users:profile',
                                    args=(request.user.username,)))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        order_id = self.kwargs.get('order_id')
        return get_object_or_404(Order, id=order_id,)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_order = self.get_object()
        order_item = OrderItem.objects.filter(order=current_order).all()
        context['order_item'] = order_item
        context['current_order'] = current_order
        return context
