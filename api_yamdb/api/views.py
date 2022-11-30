from rest_framework import viewsets


from reviews.models import UserCustomized
from .serializers import (UserSerializer,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserCustomized.objects.all()
    serializer_class = UserSerializer
