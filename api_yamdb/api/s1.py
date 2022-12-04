# Проба на добавление списка жанров

from rest_framework import serializers

from reviews.models import Category, Genre, Title

class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')

class TitlesWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = GenresSerializer(many=True)

    class Meta:
       model = Title
       fields = ('name', 'year', 'description', 'category', 'genre')
        
    def create(self, validated_data):
        genre_data = validated_data.pop('genre')     
        title = Title.objects.create(**validated_data)
        Genre.objects.create(title=title, **genre_data)
        return title

    def update(self, instance, validated_data):
        genre_data = validated_data.pop('genre')
        genre = instance.genre
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        genre.save()
        return instance