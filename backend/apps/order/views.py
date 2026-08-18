from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView , ListAPIView , RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import CheckoutSerializer , OrderSerializer 
from .services import OrderService
from .models import Order


class CheckoutView(GenericAPIView):
    serializer_class=CheckoutSerializer
    pagination_class=[IsAuthenticated]

    def post(self , request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.checkout(
            user=request.user,
            address_id=serializer.validated_data["address_id"]
        )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

class OrderListView(ListAPIView): 
    serializer_class = OrderSerializer 
    permission_classes = [IsAuthenticated] 

    def get_queryset(self): 
        return ( 
            Order.objects 
            .filter(user=self.request.user) 
            .prefetch_related( 
                "items__variant__product" 
            ) 
            .order_by("-created_at") 
        )

class OrderDetailView(RetrieveAPIView): 
    serializer_class = OrderSerializer 
    permission_classes = [IsAuthenticated] 

    def get_queryset(self): 
        return ( 
            Order.objects 
            .filter(user=self.request.user) 
            .prefetch_related( "items__variant__product" 
            ) 
        )

class CancelOrderView(APIView): 
    permission_classes = [IsAuthenticated] 

    def post(self, request, pk): 
        order = OrderService.cancel_order( request.user, pk, ) 
        return Response( 
            { 
                "message": "Order cancelled successfully.", 
                "status": order.status, 
            }, 
            status=status.HTTP_200_OK, 
        )
