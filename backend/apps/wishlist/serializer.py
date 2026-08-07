from rest_framework import serializers
from .models import WishlistItem ,Wishlist
from apps.products.serializers import ProductSummarySerializer

class AddToWishlistSerializer(serializers.Serializer):

    product_id=serializers.IntegerField()

class WishlistItemSerializer(serializers.ModelSerializer):

    product = ProductSummarySerializer(
        read_only=True
    )

    class Meta:

        model = WishlistItem

        fields = (
            "id",
            "product",
            "created_at",
        )

class WishlistSerializer(serializers.ModelSerializer):

    items = WishlistItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Wishlist

        fields = (
            "id",
            "items",
        )

class MoveToCartSerializer(serializers.Serializer):

    variant_id = serializers.IntegerField()

    quantity = serializers.IntegerField(
        min_value=1
    )