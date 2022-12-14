from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ReviewViewSet,
    CommentViewSet,
    CategoryViewSet,
    TitleViewSet,
    GenreViewSet,
    UserViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet)
router_v1.register('categories', CategoryViewSet, basename='сategories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

urlpatterns = (
    path('v1/', include(router_v1.urls)),
)
