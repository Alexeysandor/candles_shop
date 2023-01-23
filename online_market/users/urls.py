from django.contrib.auth.views import (LogoutView, PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.urls import path, reverse_lazy, include

from . import views

app_name = 'users'

# создаю пути тут, но использую их в головном views.py,
# поскольку просто наследую модели и не вижу смысла их переписывать ради того,
# чтобы использовать здесь
reset_password = [
    path('password-reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html'),
        name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete')
]

urlpatterns = [
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), 
         name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.profile_edit,
         name='profile_edit'),
    path('login/', views.loginUser, name='login'),
    path('register_done/', views.RegisterDone.as_view(), name='register_done'),
    path('reset_password/', include(reset_password))
]
