from rest_framework import viewsets
# from rest_framework.decorators import api_view
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


from reviews.models import UserCustomized
from .serializers import (
    UserSerializer,
    UserSignUpSerializer,
    TokenRequestSerializer,
    TokenResponseSerializer
)
from core.tokens import send_conf_code, code_check


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserCustomized.objects.all()
    serializer_class = UserSerializer


# class SignUp(CreateAPIView):
    '''creates new user with username and email
    and sends confirmation code to the stated email'''

    '''queryset = UserCustomized.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = (permissions.AllowAny,)
    print('wazzap')'''


class APISign_up(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_conf_code(serializer.data['username'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendToken(APIView):
    '''получает confirmation_code, проверяет его и высылает токен
    если полее некорректно - 400, если пользователь не найден - 404'''
    def post(self, request):
        data = request.data
        serializer = TokenRequestSerializer(data=data)
        '''if request.user.username not in UserCustomized:
            return Response(serializer.errors,
                            status=status.HTTP_404_NOT_FOUND)'''
        if serializer.is_valid():
            user = get_object_or_404(UserCustomized, username=data['username'])
            access_token = AccessToken.for_user(user)
            confirmation_code = data['confirmation_code']
            if not default_token_generator.check_token(
                user,
                confirmation_code
            ):
                raise ValidationError({"confirmation_code": _("Invalid token")})
            token_serializer = TokenResponseSerializer(
                data={"token": access_token}
            )
            if token_serializer.is_valid():
                print(access_token)
                return Response(data=token_serializer.data,
                                status=status.HTTP_200_OK)
            return Response(token_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
