from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from reviews.models import (
    Review,
    Comment,
    Category,
    Genre,
    Title,
    UserCustomized
)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context['view'].kwargs["title_id"]
            author = self.context['request'].user
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Нельзя создавать несколько отзывов на произведение'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = UserCustomized


class UserRoleSerializer(serializers.ModelSerializer):
    # role = serializers.CharField(read_only=True)

    class Meta:
        model = UserCustomized
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Invalid username")
        elif UserCustomized.objects.filter(username=value).exists():
            raise serializers.ValidationError("Such username already exists")
        return value

    def validate_email(self, value):
        email = value.lower()
        if UserCustomized.objects.filter(email=email).exists():
            raise serializers.ValidationError("Such email already exists")
        return email

    def create(self, validated_data):
        return UserCustomized.objects.create(**validated_data)


class TokenRequestSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField()
    username = serializers.SlugField(max_length=150)


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
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

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
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
