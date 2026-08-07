from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.products.models import ProductVariant
from .models import Cart, CartItem
from apps.shared.exceptions import OutOfStockException
from rest_framework.exceptions import ValidationError
from apps.wishlist.models import WishlistItem

class CartService:

    @staticmethod
    @transaction.atomic
    def add_to_cart(user, variant_id, quantity):

        variant = ProductVariant.objects.get(
            id=variant_id
        )

        if quantity > variant.stock:
            raise Exception("Not enough stock.")

        cart, _ = Cart.objects.get_or_create(
            user=user
        )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant
        )

        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity

        if item.quantity > variant.stock:
            raise OutOfStockException()

        item.save()

        return item

    def update_quantity(user, item_id, quantity):

        item = get_object_or_404(
            CartItem.objects.select_related("variant", "cart"),
            id=item_id,
            cart__user=user
        )

        if quantity > item.variant.stock:
            raise OutOfStockException()

        item.quantity = quantity
        item.save(update_fields=["quantity"])

        return item

    def remove_item(user, item_id):

        item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=user,
        )

        item.delete()

    def clear_cart(user):

        cart = get_object_or_404(
           Cart,
        user=user,
        )

        cart.items.all().delete()

