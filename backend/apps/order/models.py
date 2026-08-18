from django.db import models
from django.conf import settings
from apps.addresses.models import Address
from apps.products.models import ProductVariant

class Order(models.Model):

    class Status(models.TextChoices):

        PENDING = "PENDING", "Pending"

        PAID = "PAID", "Paid"

        SHIPPED = "SHIPPED", "Shipped"

        DELIVERED = "DELIVERED", "Delivered"

        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
