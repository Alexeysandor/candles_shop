from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms


class CreatingForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                        widget=forms.TextInput(attrs={'placeholder': 'MyUserName'}))
    first_name = forms.CharField(label='Имя', 
                                 max_length=20,
                                 widget=forms.TextInput(attrs={'placeholder': 'Иван'}))
    second_name = forms.CharField(label='Фамилия', 
                                 max_length=20,
                                 widget=forms.TextInput(attrs={'placeholder': 'Иванов'}))
    phone_number = forms.CharField(label='Номер телефона', 
                                 max_length=20,
                                 widget=forms.TextInput(attrs={'placeholder': '+79781234567'}))
    email = forms.EmailField(label='Адрес электронной почты',
                                 max_length=50,
                                 widget=forms.TextInput(attrs={'placeholder': 'example@gmail.com'}))
    password1 = forms.CharField(label='Пароль',
                                 max_length=50,
                                 widget=forms.TextInput(attrs={'placeholder': '12345678'}))
    password2 = forms.CharField(label='Подтвердите пароль',
                                 max_length=50,
                                 widget=forms.TextInput(attrs={'placeholder': '12345678'}))
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'second_name', 'phone_number', 'email',)


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Логин',
                                widget=forms.TextInput(attrs={'placeholder': 'example@gmail.com'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.TextInput(attrs={'placeholder': '12345678'}))
