from rest_framework import serializers
from .models import Product , ProductVariant ,ProductImage ,Brand

from apps.categories.serializers import CategorySerializer
from .service import ProductService



class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields="__all__"

class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model=ProductVariant
        fields = (
           "id",
            "sku",
            "color",
            "size",
            "price",
            "stock",
        )

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image",
            "alt_text",
            "is_primary",
        )


class ProductListSerializer(serializers.ModelSerializer):

    category = CategorySerializer()

    primary_image = serializers.SerializerMethodField()

    class Meta:

        model = Product

        fields = (
            "id",
            "name",
            "slug",
            "description",
            "category",
            "primary_image",
        )

    def get_primary_image(self, obj):

        image = obj.images.filter(
            is_primary=True
        ).first()

        if image:
            return image.image.url

        return None

class ProductDetailSerializer(serializers.ModelSerializer):

    category = CategorySerializer()

    brand = BrandSerializer()

    variants = ProductVariantSerializer(
        many=True
    )

    images = ProductImageSerializer(
        many=True
    )

    class Meta:

        model = Product

        fields = "__all__"

class ProductCreateUpdateSerializer(serializers.ModelSerializer):

    variants = ProductVariantSerializer(
        many=True
    )

    images = ProductImageSerializer(
        many=True
    )

    class Meta:

        model = Product

        fields = "__all__"

    def create(self, validated_data):

        return ProductService.create_product(
            validated_data
        )

class ProductSummarySerializer(serializers.ModelSerializer):

    brand = serializers.CharField(
        source="brand.name",
        read_only=True
    )

    category = serializers.CharField(
        source="category.name",
        read_only=True
    )

    primary_image = serializers.SerializerMethodField()

    class Meta:

        model = Product

        fields = (
            "id",
            "name",
            "slug",
            "brand",
            "category",
            "primary_image",
        )

    def get_primary_image(self, obj):

        image = obj.images.filter(
            is_primary=True
        ).first()

        if image:
            return image.image.url

        return None
    
# class ProductSerializer(serializers.ModelSerializer):

#     category = CategorySerializer(
#         read_only=True
#     )

#     brand = BrandSerializer(
#         read_only=True
#     )

#     variants = ProductVariantSerializer(
#         many=True,
#         read_only=True
#     )

#     images = ProductImageSerializer(
#         many=True,
#         read_only=True
#     )
    
#     class Meta:
#         model=Product
#         fields="__all__"

#     def create(self, validated_data):
#         return ProductService.create_product(
#             validated_data
#         )
