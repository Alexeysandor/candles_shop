from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreatingForm, LoginForm, UserProfileForm
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

    order = Order.objects.filter(user=request.user.id).all()
    return render(request, 'users/profile.html', {'user': current_username,
                                                  'order': order})


def profile_edit(request, username):
    initial_dict = {
            'first_name': request.user.first_name,
            'second_name': request.user.second_name,
            'phone_number': request.user.phone_number,
            'city': request.user.city,
            'address': request.user.address,
            'postal_code': request.user.postal_code
        }
    if request.method == 'POST':
        instance, created = CustomUser.objects.get_or_create(email=request.user.email)
        form = UserProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('users:profile', request.user.username)
    else:
        form = UserProfileForm(initial=initial_dict)
    return render(request, 'users/profile_edit.html', {'form': form})


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
