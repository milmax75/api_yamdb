from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')