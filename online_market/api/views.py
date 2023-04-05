from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.permissions import IsAdminOrReadOnly, IsAuthorOrAdmin
from api.serializers import (CartItemSerializer,CartSerializer,  OrderSerializer,
                             OrderStatusSerializer, ProductSerializer)
from shop.models import Cart, CartItem, Order, Product


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        cart, created = Cart.objects.get_or_create(user=request.user)
        quantity = int(request.query_params.get('quantity', 1))
        if CartItem.objects.filter(cart=cart, product=product).exists():
            return Response({'errors': f'{product} уже добавлена в корзину'},
                            status=status.HTTP_400_BAD_REQUEST)
        cart.add_product(product, quantity=quantity)
        return Response({'success': f'{product} успешно добавлена в корзину'},
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'],
            permission_classes=[IsAuthenticated])
    def remove_from_cart(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        cart = get_object_or_404(Cart, user=request.user)
        if not CartItem.objects.filter(cart=cart, product=product).exists():
            return Response({'errors': f'{product} уже удалена из корзины'},
                            status=status.HTTP_400_BAD_REQUEST)
        cart.remove_product(product)
        return Response({'success': f'{product} успешно удалена из корзины'},
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'],
            permission_classes=[IsAuthenticated])
    def change_quantity(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        quantity = int(request.query_params.get('quantity', 1))
        cart_item.quantity = quantity
        cart_item.save()
        return Response({'success': f'количество {product} успешно изменено на {quantity}'},
                        status=status.HTTP_200_OK)


class CartViewSet(ListAPIView, GenericViewSet):
    pagination_class = None
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def clear(self, request, *args, **kwargs):
        cart = self.get_queryset().first()
        cart.cartitem_set.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if 'pk' in self.kwargs or self.request.method == 'POST':
            return OrderSerializer
        return OrderStatusSerializer
