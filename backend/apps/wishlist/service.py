from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.products.models import Product
from .models import WishlistItem , Wishlist
from apps.cart.services import CartService


class WishlistService:
    @staticmethod
    @transaction.atomic

    def add_to_wishlist(user, product_id):

        product=get_object_or_404(
            Product,
            id=product_id,
            is_active=True
        )

        wishlist,_=Wishlist.objects.get_or_create(
            user=user
        )
        item,created = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            product=product
        )
        return item , created

    def remove_item(user, item_id):

        item = get_object_or_404(
            WishlistItem,
            id=item_id,
            wishlist__user=user,
        )

        item.delete()

    def move_to_cart(
        user,
        wishlist_item_id,
        variant_id,
        quantity,
    ):

        item = get_object_or_404(
            WishlistItem,
            id=wishlist_item_id,
            wishlist__user=user,
        )

        CartService.add_to_cart(
            user=user,
            variant_id=variant_id,
            quantity=quantity,
        )

        item.delete()

    