from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from . import views

app_name = 'shop'

cart_path = [
    path('cart', views.CartView.as_view(), name='cart_detail'),
    path('add/<product_id>/',
         views.AddProductToCartView.as_view(), name='cart_add'),
    path('update/<product_id>/',
         views.CartProductQuantityUpdateView.as_view(), name='cart_update'),
    path('remove/<product_id>/',
         views.CartProductQuantityDecreaseView.as_view(), name='cart_remove'),
    path('cart/clear/', views.ClearCartView.as_view(), name='cart_clear'),
]

order_path = [
    path('order/create/', views.OrderCreateView.as_view(),
         name='order_create'),
    path('order/created/', views.OrderCreatedView.as_view(),
         name='order_created'),
    path('order/<order_id>/', views.OrderDetailView.as_view(),
         name='order_detail'),
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('catalog', views.CatalogView.as_view(), name='catalog'),
    path('product/<slug>/', views.ProductDetailView.as_view(),
         name='product_detail'),
    path('about_us', views.AboutUsView.as_view(), name='about_us'),
    path('', include(cart_path)),
    path('', include(order_path)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
