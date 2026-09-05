from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser , FormParser

from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    DestroyAPIView,
)

from rest_framework.permissions import IsAdminUser

from .models import Product, Brand , ProductVariant ,ProductImage
from .serializers import (
    BrandSerializer,
    # ProductListSerializer,
    # ProductCreateUpdateSerializer,
    # ProductDetailSerializer,
    ProductUpdateSerializer,
    ProductCreateSerializer,
    ProductVariantUpdateSerializer,
    ProductImageSerializer,
    ProductImageUpdateSerializer,
    

)

from apps.products.models import Product
from apps.products.service import ProductService
from apps.products.serializers import ProductUpdateSerializer

from ..dashboard.serializers import AdminProductSerializer

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


# class ProductViewSet(ModelViewSet):

#     queryset = Product.objects.select_related("category", "brand").prefetch_related(
#         "variants", "images"
#     )

#     permission_classes = [IsAdminOrReadOnly]

#     def get_serializer_class(self):

#         if self.action == "list":
#             return ProductListSerializer

#         if self.action == "retrieve":
#             return ProductDetailSerializer

#         return ProductCreateUpdateSerializer


class AdminProductListCreateView(
    ListCreateAPIView
):
    permission_classes=[
        IsAdminUser
    ]

    def get_serializer_class(self):

        if self.request.method == "POST":
            return ProductCreateSerializer

        return AdminProductSerializer

    def get_queryset(self):

        return Product.objects.select_related(
            "brand",
            "category",
        ).all()


class AdminProductDetailView(RetrieveUpdateDestroyAPIView):

    permission_classes = [
        IsAdminUser
    ]

    queryset = Product.objects.select_related(
        "brand",
        "category"
    )

    serializer_class = ProductUpdateSerializer

    

    def perform_destroy(self, instance):

        ProductService.delete_product(
            instance.id
        )

class AdminVariantDetailView(
    RetrieveUpdateDestroyAPIView
):

    permission_classes = [
        IsAdminUser
    ]

    queryset = ProductVariant.objects.select_related(
        "product"
    )

    serializer_class = ProductVariantUpdateSerializer

    def perform_update(self, serializer):

        updated_variant = ProductService.update_variant(
            serializer.instance.id,
            serializer.validated_data
        )

        serializer.instance=updated_variant

    def perform_destroy(self, instance):

        ProductService.delete_variant(
            instance.id
        )


class AdminProductImageListCreateView(
   ListCreateAPIView
):

    permission_classes = [
        IsAdminUser
    ]

    serializer_class = ProductImageSerializer

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def get_queryset(self):

        product_id = self.kwargs["product_id"]

        return ProductImage.objects.filter(
            product_id=product_id
        ).order_by(
            "-is_primary",
            "id"
        )

    def perform_create(self, serializer):

        product_image = ProductService.create_product_image(
            product_id=self.kwargs["product_id"],
            image=serializer.validated_data["image" ],

            alt_text=serializer.validated_data.get(
                "alt_text",
                ""
            ),
            
            is_primary=serializer.validated_data.get(
                "is_primary",
                False
            )
        )

        serializer.instance=product_image

    

# class AdminProductImageDeleteView(
#     DestroyAPIView
# ):

#     permission_classes = [
#         IsAdminUser
#     ]

#     queryset = ProductImage.objects.all()

#     serializer_class = ProductImageSerializer

#     def perform_destroy(self, instance):

#         ProductService.delete_product_image(
#             instance.id
#         )

class AdminProductImageDetailView(
    RetrieveUpdateDestroyAPIView
):

    permission_classes = [
        IsAdminUser
    ]

    queryset = ProductImage.objects.select_related(
        "product"
    )

    serializer_class = ProductImageUpdateSerializer

    def perform_update(self, serializer):

        updated_image = ProductService.update_product_image(
            serializer.instance.id,
            serializer.validated_data
        )

        serializer.instance = updated_image

    def perform_destroy(self, instance):

        ProductService.delete_product_image(
            instance.id
        )
