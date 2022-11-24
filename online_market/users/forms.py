from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import CustomUser

from django.forms import CharField, EmailField, TextInput, PasswordInput, ValidationError, EmailInput, ModelForm
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
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2


class LoginForm(AuthenticationForm):
    username = EmailField(
        label='Адрес электронной почты',
        widget=TextInput(attrs={'placeholder': 'example@gmail.com'}))
                    
    password = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={'placeholder': '12345678'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        username_db = CustomUser.objects.filter(email=username)
        if not username_db:
            raise ValidationError('Неверный логин')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        password_db = CustomUser.objects.filter(password=password)
        if not password_db:
            raise ValidationError('Неверный пароль')
        return password


class UserProfileForm(ModelForm):
    first_name = CharField(
        label='Имя',
        required=False,
        widget=TextInput(attrs={'placeholder': 'Иван'}),
        validators=[RegexValidator(r'^[а-яА-ЯёЁa-zA-Z]+$',
                                   'Недопустимые символы'),
                    Min_Max_Length_Validator])

    second_name = CharField(
        label='Фамилия',
        required=False,
        widget=TextInput(attrs={'placeholder': 'Иванов'}),
        validators=[RegexValidator(r'^[а-яА-ЯёЁa-zA-Z]+$',
                                   'Недопустимые символы'),
                    Min_Max_Length_Validator])

    phone_number = CharField(
        label='Номер телефона',
        required=False,
        widget=TextInput(attrs={'placeholder': '+79781234567'}),
        validators=[RegexValidator(r'^\+?1?\d{10,15}$',
                                   'Введите номер телефона '
                                   'в формате "+79781234567"')])
    city = CharField(
        label='Город',
        required=False,
        max_length=50,
        widget=TextInput(attrs={'placeholder': 'Москва'}))

    address = CharField(
        label='Адрес',
        required=False,
        max_length=50,
        widget=TextInput(attrs={'placeholder': 'Красная площадь'}))

    postal_code = CharField(
        label='Почтовый индекс',
        required=False,
        max_length=6,
        widget=TextInput(attrs={'placeholder': '230035'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'second_name', 'phone_number', 'city', 'address', 'postal_code')