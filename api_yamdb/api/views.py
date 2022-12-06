from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, viewsets
from .serializers import ReviewSerializer, CommentSerializer, UserSerializer, CategoriesSerializer, GenresSerializer, TitlesCreateSerializer, TitlesReadSerializer
from reviews.models import Title, Review, UserCustomized, Category, Genre
from .permissions import IsModerOrAdmOrAuthor, IsAdminOrReadOnly
from .mixins import ProjectModelMixin
from .filters import TitlesFilter
from django.db.models import Avg


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserCustomized.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(ProjectModelMixin):
    """Категории. Чтение  - доступ без токена.
    Добавление и удаление - только администратор.
    Поиск по названию категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ProjectModelMixin):
    """Жанры. Чтение  - доступ без токена.
    Добавление и удаление - только администратор.
    Поиск по названию жанра.
    """
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)



class TitleViewSet(viewsets.ModelViewSet):
    """Произведения. Чтение  - доступ без токена.
    Добавление, обновление и удаление - только администратор.
    Фильтрация списка произведений по слагу категории, жанра,
    названию, году.
    """
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    pagination_class = pagination.LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitlesCreateSerializer
        return TitlesReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = [IsModerOrAdmOrAuthor]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    # permission_classes = [IsModerOrAdmOrAuthor]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
