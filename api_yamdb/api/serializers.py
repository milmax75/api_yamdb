from rest_framework import serializers
from review.models import Review, Comment, Category, Genre, Title
from reviews.models import UserCustomized


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = UserCustomized


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesReadSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )


class TitlesCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre')


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        title = int(data['title'])
        author = self.context['request'].user
        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                'Нельзя создавать несколько отзывов на произведение'
            )

    class Meta:
        model = Comment
        fields = '__all__'
