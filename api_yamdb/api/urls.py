from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import UserViewSet

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register('users', UserViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
