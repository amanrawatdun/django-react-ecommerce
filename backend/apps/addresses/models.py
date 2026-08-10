from django.db import models
from django.conf import settings

# Create your models here.
class Address(models.Model):

    class AddressType(models.TextChoices):
        HOME = "HOME", "Home"
        OFFICE = "OFFICE", "Office"
        OTHER = "OTHER", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="address"
    )

    full_name = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=15)

    address_line_1=models.CharField(max_length=255)

    address_line_2 = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    postal_code = models.CharField(max_length=20)

    country = models.CharField(
        max_length=100,
        default="India"
    )

    address_type = models.CharField(
        max_length=10,
        choices=AddressType.choices,
        default=AddressType.HOME
    )

    is_default = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.full_name} - {self.city}"