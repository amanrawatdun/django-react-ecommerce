from django.db.models import Count, Q, Sum

from apps.accounts.models import User
from apps.order.models import Order
from apps.products.models import Product, ProductVariant


LOW_STOCK_THRESHOLD = 5


class DashboardService:

    @staticmethod
    def get_overview():

        total_orders = Order.objects.count()

        total_customers = User.objects.filter(
            is_staff=False
        ).count()

        total_products = Product.objects.count()

        total_revenue = (
            Order.objects
            .filter(
                status=Order.Status.PAID
            )
            .aggregate(
                revenue=Sum("total_amount")
            )["revenue"]
            or 0
        )

        order_stats = Order.objects.aggregate(

            pending=Count(
                "id",
                filter=Q(
                    status=Order.Status.PENDING
                )
            ),

            paid=Count(
                "id",
                filter=Q(
                    status=Order.Status.PAID
                )
            ),

            shipped=Count(
                "id",
                filter=Q(
                    status=Order.Status.SHIPPED
                )
            ),

            delivered=Count(
                "id",
                filter=Q(
                    status=Order.Status.DELIVERED
                )
            ),

            cancelled=Count(
                "id",
                filter=Q(
                    status=Order.Status.CANCELLED
                )
            ),
        )

        inventory_stats = ProductVariant.objects.aggregate(

            low_stock=Count(
                "id",
                filter=Q(
                    stock__gt=0,
                    stock__lte=LOW_STOCK_THRESHOLD
                )
            ),

            out_of_stock=Count(
                "id",
                filter=Q(
                    stock=0
                )
            ),
        )

        return {
            "overview": {
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "total_customers": total_customers,
                "total_products": total_products,
            },

            "orders": order_stats,

            "inventory": inventory_stats,
        }