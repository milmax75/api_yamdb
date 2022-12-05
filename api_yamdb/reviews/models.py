from django.db import models
from django.contrib.auth.models import AbstractUser


class UserCustomized(AbstractUser):
    '''Детальная информация о пользователе'''
    username = models.SlugField(max_length=150,
                                unique=True,
                                blank=False,
                                null=False)
    email = models.EmailField(max_length=254, unique=True, null=False)
    first_name = models.TextField(max_length=150)
    last_name = models.TextField(max_length=150)
    bio = models.CharField(max_length=500)
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]
    role = models.CharField(max_length=10,
                            choices=ROLE_CHOICES,
                            default='user')

    def is_moderator(self):
        return self.role == self.MODERATOR

    def is_user(self):
        return self.role == self.USER

    def is_admin(self):
        return self.role == self.ADMIN
