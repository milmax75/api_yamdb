from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet  # , UserMeViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet)
# router_v1.register('users/me', UserMeViewSet, basename='me')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
