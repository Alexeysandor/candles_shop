from django.core.exceptions import ValidationError


def Min_Max_Length_Validator(value):
    min_length = 2
    max_length = 25
    if len(value) < min_length:
        raise ValidationError(f"Минимальное количество символов:{min_length}")
    if len(value) > max_length:
        raise ValidationError(f"Максимальное количество символов:{max_length}")
