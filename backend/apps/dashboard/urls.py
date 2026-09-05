from django.urls import path

from .views import (
    AdminDashboardView,
    CustomerAnalyticsView,
    LowStockVariantView,
    RecentOrdersView,
    TopProductsView,
    RevenueAnalyticsView,
    AdminOrderListView,
    AdminOrderDetailView,
    AdminOrderStatusView,
    # AdminProductListView,
    # AdminProductDetailView,
    AdminProductStatusView,
    # AdminVariantListCreateView,
    # AdminVariantUpdateView,
    # AdminVariantDeleteView,
    # AdminProductImageCreateView,
    # AdminProductImageListView,
    # AdminProductImageDeleteView,
    # AdminProductListCreateView,
)

urlpatterns = [
    path(
        "dashboard/",
        AdminDashboardView.as_view(),
        name="admin-dashboard",
    ),
    path(
        "low-stock/",
        LowStockVariantView.as_view(),
        name="low-stock",
    ),
    path(
        "recent-orders/",
        RecentOrdersView.as_view(),
        name="recent-orders",
    ),
    path(
        "top-products/",
        TopProductsView.as_view(),
        name="top-products",
    ),
    path(
        "revenue/",
        RevenueAnalyticsView.as_view(),
        name="revenue-analytics",
    ),
    path(
        "customers/",
        CustomerAnalyticsView.as_view(),
        name="customer-analytics",
    ),
    path(
        "orders/",
        AdminOrderListView.as_view(),
        name="admin-order-list",
    ),
    path(
        "orders/<int:pk>/",
        AdminOrderDetailView.as_view(),
        name="admin-order-detail",
    ),
    path(
        "orders/<int:pk>/status/",
        AdminOrderStatusView.as_view(),
        name="admin-order-status",
    ),
    # path(
    #     "products/",
    #     AdminProductListView.as_view(),
    #     name="admin-product-list",
    # ),
    # path(
    #     "remove/products/",
    #     AdminProductListCreateView.as_view(),
    #     name="admin-product-list-create",
    # ),
    # path(
    #     "products/<int:pk>/",
    #     AdminProductDetailView.as_view(),
    #     name="admin-product-detail",
    # ),
    path(
        "products/<int:pk>/status/",
        AdminProductStatusView.as_view(),
        name="admin-product-status",
    ),
    # path(
    #     "products/<int:product_id>/variants/",
    #     AdminVariantListCreateView.as_view(),
    #     name="admin-variant-list-create",
    # ),
    # path(
    #     "variants/<int:pk>/",
    #     AdminVariantUpdateView.as_view(),
    #     name="admin-variant-update",
    # ),
    # path(
    #     "variants/<int:pk>/",
    #     AdminVariantDeleteView.as_view(),
    #     name="admin-variant-delete",
    # ),
    # path(
    #     "products/<int:product_id>/images/",
    #     AdminProductImageCreateView.as_view(),
    #     name="admin-product-image-create",
    # ),
    # path(
    #     "products/<int:product_id>/image/",
    #     AdminProductImageListView.as_view(),
    #     name="admin-product-image-list",
    # ),
    # path(
    #     "images/<int:pk>/",
    #     AdminProductImageDeleteView.as_view(),
    #     name="admin-product-image-delete",
    # ),
    
]
