from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from users.models import CustomUser
from shop.models import Order
class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'order_status')

class UserSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'orders')
    
    def get_orders(self, obj):
        orders = Order.objects.filter(user=obj)
        serializer = OrderSerializer(orders, many=True)
        return serializer.data