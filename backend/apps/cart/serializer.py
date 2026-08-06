from rest_framework import serializers
from .models import CartItem ,Cart

class AddToCartSerializer(serializers.Serializer):

    variant_id = serializers.IntegerField()

    quantity = serializers.IntegerField(
        min_value=1
    )


class CartItemSerializer(serializers.ModelSerializer):

    product = serializers.CharField(
        source="variant.product.name",
        read_only=True
    )

    color = serializers.CharField(
        source="variant.color",
        read_only=True
    )

    size = serializers.CharField(
        source="variant.size",
        read_only=True
    )

    price = serializers.DecimalField(
        source="variant.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    total_price = serializers.SerializerMethodField()

    class Meta:

        model = CartItem

        fields = (
            "id",
            "product",
            "color",
            "size",
            "price",
            "quantity",
            "total_price",
        )

    def get_total_price(self, obj):

        return obj.variant.price * obj.quantity

class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        many=True,
        read_only=True
    )

    total_items = serializers.SerializerMethodField()

    grand_total = serializers.SerializerMethodField()

    class Meta:

        model = Cart

        fields = (
            "id",
            "items",
            "total_items",
            "grand_total",
        )

    def get_total_items(self, obj):

        return sum(
            item.quantity
            for item in obj.items.all()
        )

    def get_grand_total(self, obj):

        return sum(
            item.variant.price * item.quantity
            for item in obj.items.all()
        )
    
class UpdateCartItemSerializer(serializers.Serializer):

    quantity = serializers.IntegerField(
        min_value=1
    )