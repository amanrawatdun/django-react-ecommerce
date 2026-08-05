from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter

from .models import Product , Brand
from .serializers import  BrandSerializer ,ProductListSerializer , ProductCreateUpdateSerializer , ProductDetailSerializer
from ..shared.permissions import IsAdminOrReadOnly

from ..shared.pagination import DefaultPagination


# class ProductViewSet(ModelViewSet):

#     queryset = (
#         Product.objects
#         .select_related(
#             "category",
#             "brand"
#         )
#         .prefetch_related(
#             "variants",
#             "images"
#         )
#         .order_by("-created_at")
#     )

#     serializer_class=ProductSerializer

#     permission_classes=[IsAdminOrReadOnly]

#     filter_backends=[
#         DjangoFilterBackend,
#         SearchFilter,
#         OrderingFilter,
#     ]

#     filterset_fields = [
#         "category",
#         "is_active",
#     ]

#     search_fields = [
#         "name",
#         "description",
#     ]

#     ordering_fields = [
#         "created_at",
#         "name",
#     ]

#     pagination_class=DefaultPagination

#     lookup_field='slug'

class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()

    serializer_class = BrandSerializer

    permission_classes = [IsAdminOrReadOnly]

    pagination_class = DefaultPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "name",
    ]

    ordering_fields = [
        "name",
    ]

class ProductViewSet(ModelViewSet):

    queryset = (
        Product.objects
        .select_related(
            "category",
            "brand"
        )
        .prefetch_related(
            "variants",
            "images"
        )
    )

    permission_classes = [
        IsAdminOrReadOnly
    ]
    def get_serializer_class(self):

        if self.action == "list":
           return ProductListSerializer

        if self.action == "retrieve":
            return ProductDetailSerializer

        return ProductCreateUpdateSerializer
