from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title


class CategoriesSerializer(serializers.ModelSerializer):
     class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')

class TitlesReadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre')


