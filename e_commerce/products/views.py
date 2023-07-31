from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
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


@extend_schema(tags=['Category'])
class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryProductListAPIView(ListAPIView):
    serializer_class = ProductListModelSerializer
    model = Category
    product_model = Product

    def get_queryset(self):
        category_id: int = self.kwargs.get('id')
        descendant_categories = self.model.objects.get_descendants(include_self = True)
        return self.product_model.objects.filter(
            category__in=descendant_categories
        )

@extend_schema(tags=['Brand'])
class BrandModelViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class BrandProductListAPIView(ListAPIView):
    """
    - Takes id path param as brand id
    - Returns products related to brand
    """
    model = Brand
    serializer_class = ProductListModelSerializer

    def get_queryset(self):
        brand_id: int = self.kwargs.get('id')
        brand = self.model.objects.prefetch_related('products').get(pk=brand_id)
        return brand.products.all()


@extend_schema(tags=['Product'])
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListModelSerializer
        return ProductDetailModelSerializer

    def get_queryset(self):
        if self.action == 'list':
            return super().get_queryset()
        return super().get_queryset().prefetch_related('images')


class CategoryProductListAPIView(ListAPIView):
    """
    - Takes id path param as product id
    - Returns category and its ancestors or parents related to product
    """
    serializer_class = CategoryModelSerializer
    model = Product

    def get_queryset(self):
        product_id: int = self.kwargs.get('id')
        product = self.model.objects.select_related('category').get(id=product_id)
        category = product.category
        return category.get_ancestors(include_self=True)


@extend_schema(tags=['Product Image'])
class ProductImageModelViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductImageListAPIView(ListAPIView):
    """
    - Takes id path param as product id
    - Returns Images related to product
    """
    model = Product
    serializer_class = ProductImageModelSerializer

    def get_queryset(self):
        product_id: int = self.kwargs.get('id')
        product = self.model.objects.prefetch_related('images').get(pk=product_id)
        return product.images.all()
