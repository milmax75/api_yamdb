from rest_framework import serializers


from reviews.models import UserCustomized


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = UserCustomized


class UserSignUpSerializer(serializers.Serializer):

    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if (value == 'me'):
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


class TokenRequest():
    def __init__(self, confirmation_code, username):
        self.confirmation_code = confirmation_code
        self.username = username


class TokenRequestSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(read_only=True)
    username = serializers.SlugField(max_length=150, read_only=True)
