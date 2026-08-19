from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from apps.order.models import Order
from apps.order.services import OrderService
from .serializers import VerifyPaymentSerializer

class CreatePaymentView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self , request , order_id):

        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user,
        )

        if order.status != Order.Status.PENDING:
            return Response(
                {"details":"Order is not payable."},
                status=400,
            )

        data = OrderService.create_payment(order)

        return Response(data)

class VerifyPaymentView(GenericAPIView):

    serializer_class = VerifyPaymentSerializer
    permission_classes = [IsAuthenticated]

    def post(self , request , order_id):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = get_object_or_404( 
            Order, 
            id=order_id, 
            user=request.user, 
        )

        OrderService.verify_payment( 
            order, 
            serializer.validated_data, 
        ) 

        return Response({ 
            "message": "Payment verified successfully." 
        })