from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import ProductViewSet, OrderViewSet, CartViewSet

app_name = 'api'
router = DefaultRouter()

router.register('product', ProductViewSet, basename='product')
router.register('order', OrderViewSet, basename='order')
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),

]
