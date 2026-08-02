from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter

from .models import Product
from .serializers import ProductSerializer
from ..shared.permissions import IsAdminOrReadOnly

from ..shared.pagination import DefaultPagination


class ProductViewSet(ModelViewSet):

    queryset=Product.objects.all()

    serializer_class=ProductSerializer

    permission_classes=[IsAdminOrReadOnly]

    filter_backends=[
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "is_active",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "price",
        "created_at",
        "name",
    ]

    pagination_class=DefaultPagination

    lookup_field='slug'


