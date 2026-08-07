from rest_framework import status
from rest_framework.generics import GenericAPIView , RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import AddToWishlistSerializer ,WishlistSerializer ,MoveToCartSerializer
from .models import Wishlist
from .service import WishlistService


class WishlistView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        wishlist, _ = Wishlist.objects.prefetch_related(
            "items__product__brand",
            "items__product__category",
            "items__product__images",
        ).get_or_create(
            user=request.user
        )

        serializer = WishlistSerializer(wishlist)

        return Response(serializer.data)

    def post(self, request):

        serializer = AddToWishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item, created = WishlistService.add_to_wishlist(
            request.user,
            serializer.validated_data["product_id"]
        )

        if created:
            return Response(
                {"message": "Product added to wishlist."},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"message": "Product already exists in wishlist."},
            status=status.HTTP_200_OK,
        )

class RemoveWishlistItemView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        WishlistService.remove_item(
            request.user,
            pk,
        )

        return Response(
            {
                "message": "Item removed from wishlist."
            },
            status=status.HTTP_200_OK,
        )
    
class MoveWishlistItemToCartView(GenericAPIView):

    serializer_class = MoveToCartSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        WishlistService.move_to_cart(
            user=request.user,
            wishlist_item_id=pk,
            variant_id=serializer.validated_data["variant_id"],
            quantity=serializer.validated_data["quantity"],
        )

        return Response(
            {
                "message": "Item moved to cart."
            },
            status=status.HTTP_200_OK,
        )

    


