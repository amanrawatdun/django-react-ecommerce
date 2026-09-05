from rest_framework.exceptions import ValidationError
from apps.order.models import Order
from django.db import transaction
from django.shortcuts import get_object_or_404
from apps.products.models import Product

class OrderService:

    ALLOWED_TRANSITIONS = {

        Order.Status.PENDING: {
            Order.Status.PAID,
            Order.Status.CANCELLED,
        },

        Order.Status.PAID: {
            Order.Status.SHIPPED,
            Order.Status.CANCELLED,
        },

        Order.Status.SHIPPED: {
            Order.Status.DELIVERED,
        },

        Order.Status.DELIVERED: set(),

        Order.Status.CANCELLED: set(),
    }

    @staticmethod
    @transaction.atomic
    def update_status(order, new_status):

        allowed_statuses = (
            OrderService.ALLOWED_TRANSITIONS[
                order.status
            ]
        )

        if new_status not in allowed_statuses:

            raise ValidationError(
                {
                    "status": (
                        f"Cannot change order status "
                        f"from {order.status} "
                        f"to {new_status}."
                    )
                }
            )

        order.status = new_status

        order.save(
            update_fields=["status"]
        )

        return order



    