from django.core.exceptions import ValidationError
from django.utils import timezone
import re


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Неверный год. Произведения из будущего пока не принимаются.',
            params={'value': value},
        )


def validate_username(value):
    if not re.compile(r'[\w.@+-]+').match(value):
        raise ValidationError(
            'Enter a valid username',
            params={'value': value},
        )
