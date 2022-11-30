from rest_framework import serializers


from reviews.models import UserCustomized


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = UserCustomized
