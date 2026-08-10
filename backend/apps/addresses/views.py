from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Address
from .serializer import AddressSerializer
from .services import AddressService




class AddressViewSet(ModelViewSet):

    serializer_class=AddressSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        has_default = Address.objects.filter(
        user=self.request.user,
        is_default=True,
        ).exists()

        serializer.save(
        user=self.request.user,
        is_default=not has_default,
        )
    
    @action(
    detail=True,
    methods=["post"],
    url_path="set-default",
    )
    def set_default(self, request, pk=None):

        AddressService.set_default(
            user=request.user,
            address_id=pk,
        )

        return Response(
            {
             "message": "Default address updated successfully."
            },
         status=status.HTTP_200_OK,
    )



