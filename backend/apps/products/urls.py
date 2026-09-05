from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .views import (
# ProductViewSet,
BrandViewSet,
AdminProductListCreateView,
AdminProductDetailView,
AdminVariantDetailView,
AdminProductImageListCreateView,
AdminProductImageDetailView,
# AdminProductImageDeleteView,
)

router=DefaultRouter()

# router.register('products',ProductViewSet , basename='product')
router.register('brand',BrandViewSet , basename='brand')

urlpatterns=[
    # path('',include(router.urls)),

    path("admin/products",
        AdminProductListCreateView.as_view(),
        name="admin-product-list-create"
    ),
    path(
        "admin/products/<int:pk>/",
        AdminProductDetailView.as_view(),
        name="admin-product-detail"
    ),
    path(
        "admin/variants/<int:pk>/",
        AdminVariantDetailView.as_view(),
        name="admin-variant-detail"
    ),

    path(
        "admin/products/<int:product_id>/images/",
        AdminProductImageListCreateView.as_view(),
        name="admin-product-images"
    ),
    # path(
    #     "admin/images/<int:pk>/",
    #     AdminProductImageDeleteView.as_view(),
    #     name="admin-image-delete"
    # ),
    path(
        "admin/images/<int:pk>/",
        AdminProductImageDetailView.as_view(),
        name="admin-image-detail"
    ),
]