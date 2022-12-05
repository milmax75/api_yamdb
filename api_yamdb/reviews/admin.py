from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import UserCustomized

admin.site.register(UserCustomized, UserAdmin)

