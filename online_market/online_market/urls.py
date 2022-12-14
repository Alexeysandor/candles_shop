from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from users.urls import reset_password


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('', include('users.urls')),
    path('', include(reset_password))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),) 
