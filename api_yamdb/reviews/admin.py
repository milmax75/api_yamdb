from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Comment, Genre, Review, Title, UserCustomized


admin.site.register(UserCustomized, UserAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
