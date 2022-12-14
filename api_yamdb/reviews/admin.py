from django.contrib import admin
from .models import Category, Comment, Genre, Review, Title, UserCustomized
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):
    class Meta:
        model = UserCustomized
        fields = (
            'id',
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )


class UserAdmin(ImportExportModelAdmin):
    resource_classes = (UserResource,)
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'role'
    )
    list_editable = (
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    empty_value_display = '-пусто-'


admin.site.register(UserCustomized, UserAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
