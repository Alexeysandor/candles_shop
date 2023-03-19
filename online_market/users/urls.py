from django.contrib.auth.views import (LogoutView, PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.urls import include, path, reverse_lazy

from . import views

app_name = 'users'


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

auth = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('register_done/', views.RegisterDone.as_view(), name='register_done'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
]

profile = [
    path('profile/<str:username>/', views.ProfileView.as_view(),
         name='profile'),
    path('profile/<str:username>/edit/', views.ProfileEditView.as_view(),
         name='profile_edit'),
]

urlpatterns = [
    path('', include(auth)),
    path('', include(profile)),
    path('reset_password/', include(reset_password)),
]
