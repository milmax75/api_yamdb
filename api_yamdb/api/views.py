from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from django.core.exceptions import ValidationError
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist


from reviews.models import UserCustomized
from .serializers import (
    UserSerializer,
    UserSignUpSerializer,
    TokenRequestSerializer,
)
from core.tokens import send_conf_code, code_check


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserCustomized.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request, pk=None):
        user = get_object_or_404(UserCustomized,
                                 username=request.user.username)
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


'''class UserMeViewSet(viewsets.ModelViewSet):
    # queryset = UserCustomized.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    # @action(detail=False)
    def get_queryset(self):
        user = get_object_or_404(UserCustomized,
                                 username=self.request.user.username)
        return user'''


class APISign_up(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        reg_user = UserCustomized.objects.filter(username=data['username'])
        if serializer.is_valid():
            serializer.save()
            if request.user.is_anonymous:
                send_conf_code(serializer.data['username'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendToken(APIView):
    '''получает confirmation_code, проверяет его и высылает токен
    если полее некорректно - 400, если пользователь не найден - 404'''
    def post(self, request):
        data = request.data
        serializer = TokenRequestSerializer(data=data)
        if serializer.is_valid():
            user = get_object_or_404(UserCustomized, username=data['username'])
            access_token = AccessToken.for_user(user)
            confirmation_code = data['confirmation_code']
            if not default_token_generator.check_token(
                user,
                confirmation_code
            ):
                raise ValidationError({"confirmation_code": _("Invalid token")})
            return Response({'token': str(access_token)},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
