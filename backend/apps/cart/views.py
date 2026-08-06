from rest_framework.generics import GenericAPIView ,RetrieveAPIView 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializer import AddToCartSerializer , CartSerializer ,UpdateCartItemSerializer
from .services import CartService
from .models import Cart

class AddToCartView(GenericAPIView):

    serializer_class = AddToCartSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        item = CartService.add_to_cart(
            user=request.user,
            variant_id=serializer.validated_data["variant_id"],
            quantity=serializer.validated_data["quantity"],
        )

        return Response(
            {
                "message": "Item added to cart successfully.",
                "item_id": item.id,
            },
            status=status.HTTP_201_CREATED,
        )

class CartView(RetrieveAPIView):

    serializer_class = CartSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self):

        cart, _ = Cart.objects.prefetch_related("items__variant__product"
        ).get_or_create(user=self.request.user)

        return cart

class UpdateCartItemView(GenericAPIView):

    serializer_class = UpdateCartItemSerializer

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = CartService.update_quantity(
            user=request.user,
            item_id=pk,
            quantity=serializer.validated_data["quantity"],
        )

        return Response(
            {
                "message": "Quantity updated successfully.",
                "quantity": item.quantity,
            },
            status=status.HTTP_200_OK,
        )

class RemoveCartItemView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        CartService.remove_item(
            request.user,
            pk,
        )

        return Response(
            {
                "message": "Item removed successfully."
            },
            status=status.HTTP_200_OK,
        )

class ClearCartView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        CartService.clear_cart(request.user)

        return Response(
            {
                "message": "Cart cleared successfully."
            },
            status=status.HTTP_200_OK,
        )
