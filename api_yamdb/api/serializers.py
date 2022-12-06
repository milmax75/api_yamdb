from rest_framework import serializers


from reviews.models import UserCustomized


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = UserCustomized


class UserSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCustomized
        fields = ('email', 'username')

    def validate_username(self, value):
        if (value == 'me'):
            raise serializers.ValidationError('Недопустимое имя пользователя')
        return value


class TokenRequest():
    def __init__(self, confirmation_code, username):
        self.confirmation_code = confirmation_code
        self.username = username


class TokenRequestSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(read_only=True)
    username = serializers.SlugField(max_length=150, read_only=True)
