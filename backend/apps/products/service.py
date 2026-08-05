from django.db import transaction
from .models import Product ,ProductImage , ProductVariant

class ProductService:

    @classmethod
    @transaction.atomic
    def create_product(cls, validated_data):
        variants = validated_data.pop("variants", [])
        images = validated_data.pop("images", [])

        product = Product.objects.create(**validated_data)

        cls._create_variants(product, variants)
        cls._create_images(product, images)

        return product

    @staticmethod
    def _create_variants(product, variants):
        ProductVariant.objects.bulk_create(
            [
                ProductVariant(product=product, **variant)
                for variant in variants
            ]
        )

    @staticmethod
    def _create_images(product, images):
        ProductImage.objects.bulk_create(
            [
                ProductImage(product=product, **image)
                for image in images
            ]
        )
