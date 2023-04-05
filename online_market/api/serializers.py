from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from django.core.validators import RegexValidator, MinLengthValidator
from rest_framework import serializers
from users.models import CustomUser
from shop.models import Cart, CartItem, Order, OrderItem, Product


class UserRegistrationSerializer(UserCreateSerializer):
    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^[^0-9]\w*$",
                message="Имя пользователя не должно начинаться с цифр"
            )
        ]
    )
    password = serializers.CharField(
        validators=[
            MinLengthValidator(8),
        ],
        write_only=True
    )

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email',
                  'orders_count')


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'order_status')


class SpecificAndCurrentUserSerializer(serializers.ModelSerializer):
    orders = OrderStatusSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email',
                  'phone_number', 'city', 'address', 'postal_code', 'orders')


class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(write_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'image', 'price')


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id', read_only=True)
    name = serializers.CharField(source='product.name', read_only=True)
    description = serializers.CharField(source='product.description', read_only=True)
    image = serializers.ImageField(source='product.image')
    price = serializers.DecimalField(source='product.price',
                                     max_digits=10, decimal_places=2,
                                     read_only=True)
    sum_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'name', 'description', 'image', 'price', 'quantity', 'sum_price')

    def get_sum_price(self, obj):
        return obj.quantity * obj.product.price


class CartSerializer(serializers.ModelSerializer):
    cartitem_set = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['cartitem_set', 'total_price']  

    def get_total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.cartitem_set.all())
    









class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['product']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    order_status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'first_name', 'last_name', 'phone_number',
                  'city', 'address', 'postal_code', 'order_status', 'items']

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)
        if len(cart.cartitem_set.all()) < 1:
            raise serializers.ValidationError("Cart is empty")
        else:
            validated_data['user_id'] = user.id
            validated_data['email'] = user.email
            order = Order.objects.create(**validated_data)
            for item in cart.cartitem_set.all():
                OrderItem.objects.create(order=order, product=item.product,
                                         price=item.product.price)
            cart.cartitem_set.all().delete()
            return order