from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import CustomUser

from django.forms import CharField, EmailField, TextInput, PasswordInput, ValidationError, EmailInput
from .validators import Min_Max_Length_Validator


class CreatingForm(UserCreationForm):
    username = CharField(
        label='Логин',
        widget=TextInput(attrs={'placeholder': 'MyUserName'}),
        error_messages={'unique': 'Пользователь с таким логином '
                                  'уже существует'},
        validators=[RegexValidator(r'^[а-яА-ЯёЁa-zA-Z0-9]+$',
                                   'Недопустимые символы'),
                    Min_Max_Length_Validator])

    first_name = CharField(
        label='Имя',
        widget=TextInput(attrs={'placeholder': 'Иван'}),
        validators=[RegexValidator(r'^[а-яА-ЯёЁa-zA-Z]+$',
                                   'Недопустимые символы'),
                    Min_Max_Length_Validator])

    second_name = CharField(
        label='Фамилия',
        widget=TextInput(attrs={'placeholder': 'Иванов'}),
        validators=[RegexValidator(r'^[а-яА-ЯёЁa-zA-Z]+$',
                                   'Недопустимые символы'),
                    Min_Max_Length_Validator])

    phone_number = CharField(
        label='Номер телефона',
        widget=TextInput(attrs={'placeholder': '+79781234567'}),
        validators=[RegexValidator(r'^\+?1?\d{10,15}$',
                                   'Введите номер телефона '
                                   'в формате "+79781234567"')])

    email = EmailField(
        label='Адрес электронной почты',
        widget=EmailInput(attrs={'placeholder': 'example@gmail.com'}),
        error_messages={'unique': 'Пользователь с такой почтой уже существует',
                        'invalid': 'Введите корректный адрес электронной почты'})

    password1 = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={'placeholder': '12345678'}))

    password2 = CharField(
        label='Подтвердите пароль',
        widget=PasswordInput(attrs={'placeholder': '12345678'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'second_name', 'phone_number', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2


class LoginForm(AuthenticationForm):
    username = EmailField(
        label='Логин',
        widget=TextInput(attrs={'placeholder': 'example@gmail.com'}))
                    
    password = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={'placeholder': '12345678'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        username_db = CustomUser.object.filter(email=username)
        if not username_db:
            raise ValidationError('Неверный логин')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        password_db = CustomUser.object.filter(password=password)
        if not password_db:
            raise ValidationError('Неверный пароль')
        return password
