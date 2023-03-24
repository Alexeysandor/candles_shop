from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.views.generic import TemplateView
from users.urls import reset_password


urlpatterns = [
    path('admin/', admin.site.urls),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
    path('', include('shop.urls')),
    path('', include(reset_password)),
    path('', include('users.urls')),
    path('api/', include('api.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
