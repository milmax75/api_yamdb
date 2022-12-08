from rest_framework import mixins, viewsets


class ProjectModelMixin(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass
