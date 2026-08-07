from django.urls import path
from .views import WishlistView, RemoveWishlistItemView, MoveWishlistItemToCartView

urlpatterns = [
    path(
        "wishlist/",
        WishlistView.as_view(),
        name="wishlist",
    ),
    path(
        "wishlist/items/<int:pk>/",
        RemoveWishlistItemView.as_view(),
        name="remove-wishlist-item",
    ),
    path(
        "wishlist/items/<int:pk>/move-to-cart/",
        MoveWishlistItemToCartView.as_view(),
        name="move-to-cart",
    ),
] 
