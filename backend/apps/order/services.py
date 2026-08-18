from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.addresses.models import Address
from apps.cart.models import Cart
from .models import Order , OrderItem

class OrderService:
    @staticmethod
    @transaction.atomic
    def checkout(user ,address_id):

        #validate address
        address = get_object_or_404(
            Address,
            id=address_id,
            user=user,
        )

        #Load cart
        cart=get_object_or_404(
            Cart.objects.prefetch_related(
                "items__variant__product"
            ),
            user=user,
        )

        if not cart.items.exists():
            raise Exception("Cart is empty.")

        total =Decimal("0.00")

        #validate stock
        for item in cart.items.all():

            if item.quantity > item.variant.stock:
                raise Exception(
                    f"Not enough stock for {item.variant.product.name}"
                )
            total +=item.variant.price * item.quantity

        #create order
        order = Order.objects.create(
            user=user,
            address=address, 
            total_amount=total,
            )

        #create order items and reduce stock
        order_items=[]
        for item in cart.items.all(): 
            order_items.append( 
                OrderItem( 
                    order=order, 
                    variant=item.variant, 
                    quantity=item.quantity, 
                    price=item.variant.price, 
                ) 
            )

            item.variant.stock -=item.quantity
            item.variant.save(update_fields=["stock"])

        OrderItem.objects.bulk_create(order_items)

        #clear cart
        cart.items.all().delete()

        return order

    def cancel_order(user, order_id): 

        order = get_object_or_404( 
            Order.objects.prefetch_related("items__variant"), 
            id=order_id, 
            user=user, 
        ) 

        if order.status != Order.Status.PENDING: 
            raise Exception("Only pending orders can be cancelled.") 

        # Restore stock 
        for item in order.items.all(): 
            item.variant.stock += item.quantity 
            item.variant.save(update_fields=["stock"]) 

        order.status = Order.Status.CANCELLED 
        order.save(update_fields=["status"]) 

        return order