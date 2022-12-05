from rest_framework import serializers
from review.models import Review, Comment
from reviews.models import UserCustomized

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = UserCustomized


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
