from django import forms
from .models import Order

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """форма для добавления товара в корзину"""
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int, label='Количество')
    """проверка на то, что товар попал в корзину, скрыто для юзеров"""
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Имя',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Иван'}))

    second_name = forms.CharField(
        label='Фамилия',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Иванов'}))

    phone_number = forms.CharField(
        label='Номер телефона',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': '+79781234567'}))
    email = forms.EmailField(
        label='Электронная почта',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'example@gmail.com'}),
        error_messages={'invalid': 'Email: Неверно заполнено'})
    
    city = forms.CharField(
        label='Город',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Москва'}))

    address = forms.CharField(
        label='Адрес',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Красная площадь'}))

    postal_code = forms.CharField(
        label='Почтовый индекс',
        max_length=6,
        widget=forms.TextInput(attrs={'placeholder': '230035'}))

    class Meta:
        model = Order
        fields = ('first_name', 'second_name', 'phone_number', 'email', 'city', 'address', 'postal_code')
