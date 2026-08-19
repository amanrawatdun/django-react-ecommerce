from django.db import transaction

from apps.order.services import client
from apps.order.models import Order
from apps.payment.models import Payment


@staticmethod
@transaction.atomic

def verify_payment(order , data):

    client.utility.verify_payment_signature({
        "razorpay_order_id": data["razorpay_order_id"],
        "razorpay_payment_id": data["razorpay_payment_id"],
        "razorpay_signature": data["razorpay_signature"],
    })

    payment = order.payment

    payment.razorpay_payment_id = data["razorpay_payment_id"]
    payment.razorpay_signature = data["razorpay_signature"]
    payment.status = Payment.Status.SUCCESS
    payment.save()

    order.status = Order.status.PAID
    order.save(update_fields=["status"])

    return payment