from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import CommonPasswordValidator, NumericPasswordValidator, MinimumLengthValidator, UserAttributeSimilarityValidator
from difflib import SequenceMatcher
from django.core.validators import MinLengthValidator
from .models import CustomUser
import re


class CustomMinimumLengthPasswordValidator(MinimumLengthValidator):
    """валидатор для проверки длины пароля"""
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError('Пароль должен состоять'
                                  ' минимум из %(min_length)d символов',
                                  code='short',
                                  params={'min_length': self.min_length})


class CustomNumericPasswordValidator(NumericPasswordValidator):
    """Валидатор для проверки чтобы пароль не состоял из одних чисел"""
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError("Пароль не может состоять только из чисел",
                                  code='password_entirely_numeric')


class CustomCommonPasswordValidator(CommonPasswordValidator):
    """Валидатор для проверки простоты пароля"""
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError("Ваш пароль слишком простой",
                                  code='password_too_common')


class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):

    def validate(self, password, user=None):
        if not user:
            return
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    raise ValidationError(
                        ("Пароль не может совпадать с полем %(verbose_name)s."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )


def Min_Max_Length_Validator(value):
    min_length = 2
    max_length = 25
    if len(value) < min_length:
        raise ValidationError(f"Минимальное количество символов:{min_length}")
    if len(value) > max_length:
        raise ValidationError(f"Максимальное количество символов:{max_length}")


