from django import forms

from .models import Order

# генератор для добавления товара в количестве от 1 до 20
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """форма для добавления товара в корзину"""
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int, label='Количество')
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):
    """форма оформления заказа"""
    first_name = forms.CharField(
        label='Имя',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Иван'}))

    last_name = forms.CharField(
        label='Фамилия',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Иванов'}))

    phone_number = forms.CharField(
        label='Номер телефона',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': '+79781234567'}))

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
        fields = ('first_name', 'last_name', 'phone_number',
                  'city', 'address', 'postal_code')
