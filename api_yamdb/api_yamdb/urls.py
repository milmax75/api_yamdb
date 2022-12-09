from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from api.views import APISign_up, SendToken


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),

    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/signup/', APISign_up.as_view()),
    path('api/v1/auth/token/', SendToken.as_view()),
]
