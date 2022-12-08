from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, permissions, status
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
    TitlesReadSerializer
)
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

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
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


class APISign_up(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if request.user.is_anonymous:
                send_conf_code(serializer.data['username'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendToken(APIView):
    '''получает confirmation_code, проверяет его и высылает токен
    если полее некорректно - 400, если пользователь не найден - 404'''

    permission_classes = (permissions.AllowAny,)

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
                raise ValidationError(
                    {"confirmation_code": _("Invalid token")})
            return Response({'token': str(access_token)},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(ProjectModelMixin):
    """Категории. Чтение  - доступ без токена.
    Добавление и удаление - только администратор.
    Поиск по названию категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ProjectModelMixin):
    """Жанры. Чтение  - доступ без токена.
    Добавление и удаление - только администратор.
    Поиск по названию жанра.
    """
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Произведения. Чтение  - доступ без токена.
    Добавление, обновление и удаление - только администратор.
    Фильтрация списка произведений по слагу категории, жанра,
    названию, году.
    """
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
    permission_classes = [IsModerOrAdmOrAuthor]
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
    permission_classes = [IsModerOrAdmOrAuthor]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
