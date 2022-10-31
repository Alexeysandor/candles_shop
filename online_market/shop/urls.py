from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='home'),
    path('product/<slug>/', views.product_detail, name='product_detail'),
    path('catalog', views.catalog, name='catalog'),
    path('about_us', views.about_us, name='about_us'),
    path('cart', views.cart_detail, name='cart_detail'),
    path('add/<product_id>/', views.cart_add, name='cart_add'),
    path('remove/<product_id>/', views.cart_remove, name='cart_remove'),
    path('update/<product_id>/', views.cart_update, name='cart_update'),
    path('order/', views.order_create, name='order'),
    path('order_list/', views.order_list, name='order_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
