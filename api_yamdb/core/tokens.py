from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from reviews.models import UserCustomized


def send_conf_code(username):
    user = UserCustomized.objects.get(username=username)
    confirmation_code = default_token_generator.make_token(user)
    subject = 'Your confirmation code'
    message = confirmation_code
    send_mail(subject, message, None, [user.email], fail_silently=False,)
