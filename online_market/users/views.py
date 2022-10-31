from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreatingForm, LoginForm
from .models import CustomUser
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView


class SignUp(CreateView):
    form_class = CreatingForm
    success_url = reverse_lazy('shop:catalog')
    template_name = 'users/signup.html'


@login_required
def profile(request, username):
    current_username = get_object_or_404(CustomUser, username=username)
    return render(request, 'users/profile.html', {'user': current_username})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("shop:home")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


class RegisterDone(TemplateView):
    template_name = 'users/register_done.html'
