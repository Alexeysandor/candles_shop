from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.base import TemplateView

from .forms import CreatingForm, LoginForm, UserProfileForm
from .models import CustomUser


class SignUp(CreateView):
    template_name = 'users/signup.html'
    form_class = CreatingForm
    success_url = reverse_lazy('users:register_done')


class RegisterDone(TemplateView):
    template_name = 'users/register_done.html'


class LoginUserView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('users:profile',
                            args=(self.request.user.username,))


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = CustomUser.objects.prefetch_related('orders')
    paginate_by = settings.PRODUCT_COUNT

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect(reverse('users:login'))
        if self.request.user.username != self.kwargs['username']:
            return redirect(reverse('users:profile',
                                    args=(request.user.username,)))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = self.request.user.orders.all()
        context['order'] = orders
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'users/profile_edit.html'
    form_class = UserProfileForm
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        return CustomUser.objects.filter(email=self.request.user.email)

    def get_success_url(self):
        return reverse_lazy('users:profile',
                            args=(self.request.user.username,))
