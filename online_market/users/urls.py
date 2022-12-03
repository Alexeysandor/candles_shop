from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
app_name = 'users'

urlpatterns = [
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.profile_edit, name='profile_edit'),
    path('login/', views.loginUser, name='login'),
    path('register_done/', views.RegisterDone.as_view(), name='register_done'),
    
]
