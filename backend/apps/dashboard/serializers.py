from rest_framework import serializers
from apps.products.models import ProductVariant , Product
from apps.order.models import Order


class LowStockVariantSerializer(serializers.ModelSerializer):

    product = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = ProductVariant

        fields = (
            "id",
            "product",
            "sku",
            "color",
            "size",
            "stock",
            "price",
        )

class AdminRecentOrderSerializer(serializers.ModelSerializer):

    customer = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Order

        fields = (
            "id",
            "customer",
            "status",
            "total_amount",
            "created_at",
        )

class TopProductSerializer(serializers.Serializer):

    product = serializers.CharField(
        source="name"
    )

    units_sold = serializers.IntegerField()

class DailyRevenueSerializer(serializers.Serializer):

    date = serializers.DateField()

    revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

class UpdateOrderStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=Order.Status.choices
    )

class AdminOrderSerializer(serializers.ModelSerializer):

    customer = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:

        model = Order

        fields = (
            "id",
            "customer",
            "status",
            "total_amount",
            "created_at",
        )


class AdminProductSerializer(serializers.ModelSerializer):

    brand_name = serializers.CharField(
        source="brand.name",
        read_only=True
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:

        model = Product

        fields = (
            "id",
            "name",
            "slug",
            "description",
            "brand",
            "brand_name",
            "category",
            "category_name",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "slug",
            "created_at",
            "updated_at",
        )

