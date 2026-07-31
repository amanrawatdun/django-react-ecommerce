from rest_framework.viewsets import ModelViewSet

from .models import Category
from .serializers import CategorySerializer
from .permissions import IsAdminOrReadOnly
from .pagination import CategoryPagination


class CategoryViewSet(ModelViewSet):

    queryset=Category.objects.all()

    serializer_class=CategorySerializer

    permission_classes=[IsAdminOrReadOnly]

    lookup_field='slug'

    search_fields=['name']

    ordering_fields=["name","created_at"]

    pagination_class=CategoryPagination
