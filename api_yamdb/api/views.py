from rest_framework import filters, pagination, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from .filters import TitlesFilter
from .mixins import ProjectModelMixin
from reviews.models import Category, Genre, Title
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesReadSerializer,
                          TitlesCreateSerializer)

class CategoryViewSet(ProjectModelMixin):
    """Категории. Чтение  - доступ без токена.
    Добавление и удаление - только администратор.
    Поиск по названию категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class GenreViewSet (ProjectModelMixin):
    """Жанры. Чтение  - доступ без токена.
    Добавление и удаление - только администратор.
    Поиск по названию жанра.
    """
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class TitleViewSet(viewsets.ModelViewSet):
    """Произведения. Чтение  - доступ без токена.
    Добавление, обновление и удаление - только администратор.
    Фильтрация списка произведений по слагу категории, жанра,
    названию, году.
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('rating')
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitlesFilter
    pagination_class = (pagination.LimitOffsetPagination)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitlesCreateSerializer
        return TitlesReadSerializer
