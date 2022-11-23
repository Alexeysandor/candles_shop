from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreatingForm, LoginForm
from .models import CustomUser
from shop.models import Order
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView


class SignUp(CreateView):
    form_class = CreatingForm
    success_url = reverse_lazy('users:register_done')
    template_name = 'users/signup.html'


@login_required
def profile(request, username):
    current_username = get_object_or_404(CustomUser, username=username)
    order = Order.objects.filter(email=request.user.email).all()
    return render(request, 'users/profile.html', {'user': current_username,
                                                  'order': order})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('users:profile', request.user.username)
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


class RegisterDone(TemplateView):
    template_name = 'users/register_done.html'
