from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
<<<<<<< HEAD
     if value > timezone.now().year:
        raise ValidationError(
            'Неверный год. Произведения из будущего пока не принимаются.',
            params={'value': value},
        )
=======
    if value > timezone.now().year:
        raise ValidationError(
            'Неверный год. Произведения из будущего пока не принимаются.',
            params={'value': value},
        )
>>>>>>> feature/Category_Genre_Title
