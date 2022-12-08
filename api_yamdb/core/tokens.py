from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from reviews.models import UserCustomized


def send_conf_code(username):
    user = UserCustomized.objects.get(username=username)
    confirmation_code = default_token_generator.make_token(user)
    subject = 'Your confirmation code'
    message = confirmation_code
    email_from = 'admin@admin.com'
    send_mail(subject, message, email_from, [user.email], fail_silently=False,)
