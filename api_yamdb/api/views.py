from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    UserSerializer,
    UserSignUpSerializer,
    TokenRequestSerializer,
    ReviewSerializer,
    CommentSerializer,
    CategoriesSerializer,
    GenresSerializer,
    TitlesCreateSerializer,
    TitlesReadSerializer,
    UserRoleSerializer
)
from django.db import IntegrityError
from core.tokens import send_conf_code
from reviews.models import Title, Review, UserCustomized, Category, Genre, \
    UserCustomized
from .permissions import IsModerOrAdmOrAuthor, IsAdminOrReadOnly, IsAdmin
from .mixins import ProjectModelMixin
from .filters import TitlesFilter
from django.db.models import Avg


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserCustomized.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    def create_user(username, email, first_name, last_name, bio, role):
        user = UserCustomized(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            role=role
        )
        user.set_unusable_password()
        user.save()
        return user

    @action(detail=False, methods=('get', 'patch'),
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        user = get_object_or_404(UserCustomized,
                                 username=request.user.username)
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if not (self.request.user.is_admin or self.request.user.is_superuser):
            serializer = UserRoleSerializer(user, data=request.data,
                                            partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APISignUp(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        try:
            obj, created = UserCustomized.objects.get_or_create(
                email=email,
                username=username
            )
        except IntegrityError:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_anonymous or created is not True:
            send_conf_code(serializer.data['username'])
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        serializer = TokenRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserCustomized,
                                 username=data.get('username'))
        access_token = AccessToken.for_user(user)
        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(
                user,
                confirmation_code
        ):
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'token': str(access_token)},
                        status=status.HTTP_200_OK)


class CategoryViewSet(ProjectModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenreViewSet(ProjectModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("year")
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitlesCreateSerializer
        return TitlesReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModerOrAdmOrAuthor,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsModerOrAdmOrAuthor,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
