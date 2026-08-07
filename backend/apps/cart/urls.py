from django.urls import path

from .views import (
    AddToCartView,
    CartView,
    UpdateCartItemView,
    RemoveCartItemView,
    ClearCartView,
)

urlpatterns = [
    path(
        "cart/add/",
        AddToCartView.as_view(),
        name="add-to-cart",
    ),
    path(
        "cart/",
        CartView.as_view(),
        name="cart",
    ),
    path(
        "cart/items/<int:pk>/",
        UpdateCartItemView.as_view(),
        name="update-cart-item",
    ),
    path(
        "cart/items/<int:pk>/",
        RemoveCartItemView.as_view(),
        name="remove-cart-item",
    ),
    path(
        "cart/clear/",
        ClearCartView.as_view(),
        name="clear-cart",
    ),
]
