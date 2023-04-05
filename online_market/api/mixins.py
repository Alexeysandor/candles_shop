from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet


class ListRetrieveViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    pass


class ListUpdateViewSet(ListModelMixin, UpdateModelMixin, GenericViewSet):
    pass