from rest_framework import serializers
from .models import OrderItem , Order


class CheckoutSerializer(serializers.Serializer):

    address_id = serializers.IntegerField()


class OrderItemSerializer(serializers.ModelSerializer):

    product = serializers.CharField(source="variant.product.name", read_only=True)

    color = serializers.CharField(source="variant.color", read_only=True)
   
    size = serializers.CharField(source="variant.size", read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "color",
            "size",
            "price",
            "quantity",
        )

class OrderSerializer(serializers.ModelSerializer): 
    items = OrderItemSerializer( many=True, read_only=True ) 
    class Meta: 
        model = Order 
        fields = ( "id", "status", "total_amount", "created_at", "items", )  

