from rest_framework.viewsets import ModelViewSet
from .serializers import (
    CategoryModelSerializer,
    BrandModelSerializer,
    ProductDetailModelSerializer,
    ProductListModelSerializer,
    ProductImageModelSerializer,
)
from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
)
from ..core.permissions import IsAdminOrReadOnly


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class BrandModelViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListModelSerializer
        return ProductDetailModelSerializer


class ProductImageModelViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageModelSerializer
    permission_classes = [IsAdminOrReadOnly]
