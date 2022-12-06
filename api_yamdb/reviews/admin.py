from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, UserCustomized

admin.site.register(UserCustomized)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)