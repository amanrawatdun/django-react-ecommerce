from django.db import transaction
from .models import Product ,ProductImage , ProductVariant
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from ..order.models import OrderItem
class ProductService:

    
    # def create_product(cls, validated_data):
    #     variants = validated_data.pop("variants", [])
    #     images = validated_data.pop("images", [])

    #     product = Product.objects.create(**validated_data)

    #     cls._create_variants(product, variants)
    #     cls._create_images(product, images)

    #     return product
    @staticmethod
    def create_product(product_data, variants_data=None):

        variants_data = variants_data or []

        with transaction.atomic():

            # Create Product
            product = Product.objects.create(
                **product_data
            )

            # Create Product Variants
            for variant_data in variants_data:

                ProductVariant.objects.create(
                    product=product,
                    **variant_data
                )

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

    @staticmethod
    def create_variant(
        product_id,
        validated_data
    ):

        product = get_object_or_404(
            Product,
            id=product_id
        )

        variant = ProductVariant.objects.create(
            product=product,
            **validated_data
        )

        return variant


    @staticmethod
    def set_active(
        product_id,
        is_active
    ):

        product = get_object_or_404(
            Product,
            id=product_id
        )

        product.is_active = is_active
        product.save(
            update_fields=["is_active"]
        )

        return product

    @staticmethod
    def delete_product_image(image_id):

        with transaction.atomic():

            product_image = get_object_or_404(
                ProductImage,
                id=image_id
            )

            product = product_image.product

            was_primary = product_image.is_primary

            product_image.delete()

        # If deleted image was primary,
        # promote another image.
            if was_primary:

                next_image = ProductImage.objects.filter(
                    product=product
                ).order_by("id").first()

                if next_image:

                    next_image.is_primary = True

                    next_image.save(
                        update_fields=["is_primary"]
                    )

        return True

    @staticmethod
    def create_product_image(
        product_id,
        image,
        alt_text="",
        is_primary=False
    ):

        product = get_object_or_404(
            Product,
            id=product_id
        )

        with transaction.atomic():

        # If this image is primary,
        # remove primary status from existing images.
            if is_primary:

                ProductImage.objects.filter(
                    product=product,
                    is_primary=True
                ).update(
                    is_primary=False
                )

        # If this is the first image,
        # automatically make it primary.
            has_images = ProductImage.objects.filter(
                product=product
            ).exists()

            if not has_images:

                is_primary = True

            product_image = ProductImage.objects.create(
                product=product,
                image=image,
                alt_text=alt_text,
                is_primary=is_primary
            )

        return product_image


    @staticmethod
    def update_product_image(
        image_id,
        validated_data
    ):

        with transaction.atomic():

            product_image = get_object_or_404(
                ProductImage,
                id=image_id
            )

        # Check if admin is making this image primary
            is_primary = validated_data.get(
                "is_primary",
                product_image.is_primary
            )

            if is_primary:

                ProductImage.objects.filter(
                    product=product_image.product,
                    is_primary=True
                ).exclude(
                    id=product_image.id
                ).update(
                    is_primary=False
                )

        # Update fields
            for field, value in validated_data.items():

                setattr(
                    product_image,
                    field,
                    value
                )

            product_image.save()

        return product_image


    @staticmethod
    def update_variant(variant_id, validated_data):

        variant = get_object_or_404(
            ProductVariant,
            id=variant_id
        )

        for field, value in validated_data.items():

            setattr(
                variant,
                field,
                value
            )

        variant.save()

        return variant

    @staticmethod
    def delete_variant(variant_id):

        variant = get_object_or_404(
            ProductVariant,
            id=variant_id
        )

    # Check whether this variant has been used in an order
        has_orders = OrderItem.objects.filter(
            variant=variant
        ).exists()

        if has_orders:

            raise ValidationError(
                "This variant cannot be deleted because it "
                "has already been used in an order."
            )

        variant.delete()

  