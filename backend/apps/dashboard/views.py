from django.db.models import Sum, Q
from django.db.models.functions import TruncDate
from django.utils import timezone

from datetime import timedelta

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    GenericAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView
)


from apps.accounts.models import User
from apps.order.models import Order
from apps.products.models import Product, ProductVariant ,ProductImage
from .serializers import (
    DailyRevenueSerializer,
    LowStockVariantSerializer,
    AdminRecentOrderSerializer,
    TopProductSerializer,
    AdminOrderSerializer,
    UpdateOrderStatusSerializer,
    AdminProductSerializer,
   
)

from apps.products.serializers import (
    ProductStatusSerializer,
    ProductImageSerializer,
    ProductUpdateSerializer

)
from .selectors import DashboardService
from apps.order.services import OrderService
from django.shortcuts import get_object_or_404

# from .services import ProductService
from apps.products.service import ProductService
from apps.products.serializers import ProductVariantSerializer , ProductCreateSerializer

LOW_STOCK_THRESHOLD = 5


class AdminDashboardView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        data = DashboardService.get_overview()

        return Response(data)


class LowStockVariantView(ListAPIView):

    serializer_class = LowStockVariantSerializer

    permission_classes = [IsAdminUser]

    def get_queryset(self):

        return (
            ProductVariant.objects.select_related("product")
            .filter(
                stock__gt=0,
                stock__lte=5,
                product__is_active=True,
            )
            .order_by("stock")
        )


class RecentOrdersView(ListAPIView):

    serializer_class = AdminRecentOrderSerializer

    permission_classes = [IsAdminUser]

    def get_queryset(self):

        return Order.objects.select_related("user").order_by("-created_at")[:10]


class TopProductsView(ListAPIView):

    serializer_class = TopProductSerializer

    permission_classes = [IsAdminUser]

    def get_queryset(self):

        return (
            Product.objects.annotate(units_sold=Sum("variants__order_items__quantity"))
            .filter(units_sold__isnull=False)
            .order_by("-units_sold")[:10]
        )


class RevenueAnalyticsView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        today = timezone.localdate()

        paid_statuses = [
            Order.Status.PAID,
            Order.Status.SHIPPED,
            Order.Status.DELIVERED,
        ]

        today_revenue = (
            Order.objects.filter(
                status__in=paid_statuses,
                created_at__date=today,
            ).aggregate(total=Sum("total_amount"))["total"]
            or 0
        )

        week_start = today - timedelta(days=6)

        this_week_revenue = (
            Order.objects.filter(
                status__in=paid_statuses,
                created_at__date__gte=week_start,
                created_at__date__lte=today,
            ).aggregate(total=Sum("total_amount"))["total"]
            or 0
        )

        month_start = today.replace(day=1)

        this_month_revenue = (
            Order.objects.filter(
                status__in=paid_statuses,
                created_at__date__gte=month_start,
                created_at__date__lte=today,
            ).aggregate(total=Sum("total_amount"))["total"]
            or 0
        )

        daily_revenue = (
            Order.objects.filter(
                status__in=paid_statuses,
                created_at__date__gte=week_start,
                created_at__date__lte=today,
            )
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(revenue=Sum("total_amount"))
            .order_by("date")
        )

        return Response(
            {
                "summary": {
                    "today": today_revenue,
                    "this_week": this_week_revenue,
                    "this_month": this_month_revenue,
                },
                "daily_revenue": DailyRevenueSerializer(daily_revenue, many=True).data,
            }
        )


class CustomerAnalyticsView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        today = timezone.localdate()

        total_customers = User.objects.filter(is_staff=False).count()

        week_start = today - timedelta(days=6)

        new_this_week = User.objects.filter(
            is_staff=False,
            date_joined__date__gte=week_start,
            date_joined__date__lte=today,
        ).count()

        month_start = today.replace(day=1)

        new_this_month = User.objects.filter(
            is_staff=False,
            date_joined__date__gte=month_start,
            date_joined__date__lte=today,
        ).count()

        return Response(
            {
                "total_customers": total_customers,
                "new_this_week": new_this_week,
                "new_this_month": new_this_month,
            }
        )


class AdminOrderListView(ListAPIView):

    serializer_class = AdminOrderSerializer

    permission_classes = [IsAdminUser]

    def get_queryset(self):

        return Order.objects.select_related("user").order_by("-created_at")


class AdminOrderDetailView(RetrieveAPIView):

    serializer_class = AdminOrderSerializer

    permission_classes = [IsAdminUser]

    def get_queryset(self):

        return Order.objects.select_related("user").prefetch_related(
            "items__variant__product"
        )


class AdminOrderStatusView(GenericAPIView):

    serializer_class = UpdateOrderStatusSerializer

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        order = get_object_or_404(Order, id=pk)

        updated_order = OrderService.update_status(
            order=order,
            new_status=serializer.validated_data["status"],
        )

        return Response(AdminOrderSerializer(updated_order).data)


# class AdminProductListView(ListAPIView):

#     serializer_class = AdminProductSerializer

#     permission_classes = [IsAdminUser]

#     def get_queryset(self):

#         queryset = Product.objects.select_related(
#             "brand",
#             "category",
#         ).order_by("-created_at")

#         search = self.request.query_params.get("search")

#         category = self.request.query_params.get("category")

#         brand = self.request.query_params.get("brand")

#         is_active = self.request.query_params.get("is_active")

#         if search:

#             queryset = queryset.filter(
#                 Q(name__icontains=search) | Q(description__icontains=search)
#             )

#         if category:

#             queryset = queryset.filter(category_id=category)

#         if brand:

#             queryset = queryset.filter(brand_id=brand)

#         if is_active is not None:

#             queryset = queryset.filter(is_active=is_active.lower() == "true")

#         return queryset


# class AdminProductCreateView(CreateAPIView):

#     serializer_class = ProductCreateSerializer

#     permission_classes = [
#         IsAdminUser
#     ]

# class AdminProductListCreateView(
#     ListCreateAPIView
# ):
#     permission_classes=[
#         IsAdminUser
#     ]

#     def get_serializer_class(self):

#         if self.request.method == "POST":
#             return ProductCreateSerializer

#         return AdminProductSerializer

#     def get_queryset(self):

#         return Product.objects.select_related(
#             "brand",
#             "category"
#         ).all()

# class AdminProductDetailView(RetrieveUpdateDestroyAPIView):

#     serializer_class = AdminProductSerializer

#     permission_classes = [IsAdminUser]

#     queryset = Product.objects.select_related(
#         "brand",
#         "category",
#     )
#     serializer_class = ProductUpdateSerializer

#     def perform_destroy(self, instance):

#         ProductService.delete_product(
#             instance.id
#         )


class AdminProductStatusView(GenericAPIView):

    serializer_class = ProductStatusSerializer

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        product = ProductService.set_active(
            product_id=pk,
            is_active=serializer.validated_data["is_active"],
        )

        return Response(AdminProductSerializer(product).data)


# class AdminVariantListCreateView(ListCreateAPIView):

#     serializer_class = ProductVariantSerializer

#     permission_classes = [IsAdminUser]

#     def get_queryset(self):

#         return (
#             ProductVariant.objects.filter(product_id=self.kwargs["product_id"])
#             .select_related("product")
#             .order_by("id")
#         )

#     def perform_create(self, serializer):

#         ProductService.create_variant(
#             product_id=self.kwargs["product_id"],
#             validated_data=serializer.validated_data,
#         )

# class AdminVariantUpdateView(UpdateAPIView):

#     serializer_class = ProductVariantSerializer

#     permission_classes = [
#         IsAdminUser
#     ]

#     queryset = ProductVariant.objects.all()

# class AdminVariantDeleteView(DestroyAPIView):

#     permission_classes = [
#         IsAdminUser
#     ]

#     queryset = ProductVariant.objects.all()

# class AdminProductImageCreateView(CreateAPIView):

#     serializer_class = ProductImageSerializer

#     permission_classes = [
#         IsAdminUser
#     ]

#     def perform_create(self, serializer):

#         ProductService.create_product_image(
#             product_id=self.kwargs["product_id"],
#             validated_data=serializer.validated_data,
#         )

# class AdminProductImageCreateView(CreateAPIView):

#     serializer_class = ProductImageSerializer

#     permission_classes = [
#         IsAdminUser
#     ]

#     def perform_create(self, serializer):

#         ProductService.create_product_image(
#             product_id=self.kwargs["product_id"],
#             validated_data=serializer.validated_data,
#         )


# class AdminProductImageListView(ListAPIView):

#     serializer_class = ProductImageSerializer

#     permission_classes = [
#         IsAdminUser
#     ]

#     def get_queryset(self):

#         return (
#             ProductImage.objects
#             .filter(
#                 product_id=self.kwargs["product_id"]
#             )
#             .order_by("-is_primary", "-created_at")
#         )

# class AdminProductImageDeleteView(DestroyAPIView):

#     permission_classes = [
#         IsAdminUser
#     ]

#     queryset = ProductImage.objects.all()
