from django.contrib import admin
<<<<<<< HEAD

from django.contrib.auth.admin import UserAdmin
from .models import UserCustomized

admin.site.register(UserCustomized, UserAdmin)

=======
from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
        'genre'
    )
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
>>>>>>> feature/Category_Genre_Title
