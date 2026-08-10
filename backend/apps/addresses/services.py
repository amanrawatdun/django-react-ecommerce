from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Address


class AddressService:

    @staticmethod
    @transaction.atomic
    def set_default(user, address_id):

        address = get_object_or_404(
            Address,
            id=address_id,
            user=user,
        )

        Address.objects.filter(
            user=user,
            is_default=True,
        ).update(
            is_default=False
        )

        address.is_default = True
        address.save(update_fields=["is_default"])

        return address
