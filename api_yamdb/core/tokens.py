from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from reviews.models import UserCustomized
from rest_framework_simplejwt.tokens import AccessToken
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


def send_conf_code(username):
    user = UserCustomized.objects.get(username=username)
    confirmation_code = default_token_generator.make_token(user)
    print(confirmation_code)
    subject = 'Your confirmation code'
    message = confirmation_code
    email_from = 'admin@admin.com'
    send_mail(subject, message, email_from, [user.email], fail_silently=False,)


def code_check(username, confirmation_code):
    user = get_object_or_404(UserCustomized, username=username)
    access_token = AccessToken.for_user(user)
    if not default_token_generator.check_token(
        user,
        confirmation_code
    ):
        raise ValidationError({"confirmation_code": _("Invalid token")})
    return Response({'token': str(access_token)},
                    status=status.HTTP_200_OK)
