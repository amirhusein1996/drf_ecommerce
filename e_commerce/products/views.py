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

    """
    ## Category Model Viewset
    - Handles CRUD operations for Categories.


    Includes permissions to only allow admin users to create, update and delete categories
    while allowing read-only access to non-admin users.
    """

    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(tags=['Category', 'Product'])
class CategoryProductListAPIView(ListAPIView):

    """
    ## List API View to retrieve Products for a Category and its descendant categories.
    - Takes the category ID as a path parameter and returns all products
        belonging to that category and its descendant categories.
    - Uses ProductListModelSerializer to serialize the product list.
    """

    serializer_class = ProductListModelSerializer
    model = Category
    product_model = Product

    def get_queryset(self):
        category_id: int = self.kwargs.get('id')
        descendant_categories = self.model.objects.get(id=category_id).get_descendants(include_self=True)
        return self.product_model.objects.filter(
            category__in=descendant_categories
        )


@extend_schema(tags=['Brand'])
class BrandModelViewSet(ModelViewSet):

    """
    ## Brand Model Viewset
    - Handles CRUD operations for Brands.


    Includes permissions to only allow admin users to create, update and delete categories
    while allowing read-only access to non-admin users.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(tags=['Brand', 'Product'])
class BrandProductListAPIView(ListAPIView):

    """
    ## List API View to retrieve Products for a Brand.
    - Takes the brand ID as a path parameter and returns all products
        belonging to that brand.
    - Uses ProductListModelSerializer to serialize the product list.
    """

    model = Brand
    serializer_class = ProductListModelSerializer

    def get_queryset(self):
        brand_id: int = self.kwargs.get('id')
        brand = self.model.objects.prefetch_related('products').get(pk=brand_id)
        return brand.products.all()


@extend_schema(tags=['Product'])
class ProductModelViewSet(ModelViewSet):

    """
    ## Product Model Viewset
    - Handles CRUD operations for Products.
    #### Depending on the action, uses a different serializer class:
    - For 'list' action, uses ProductListModelSerializer which
    contains a minimal set of fields
    - For all other actions, uses ProductDetailModelSerializer which
    contains all relevant fields


    Includes permissions to only allow admin users to create, update and delete products
    while allowing read-only access to non-admin users.
    """

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


@extend_schema(tags=['Category', 'Product'])
class ProductCategoryListAPIView(ListAPIView):

    """
    ## List API View to retrieve Categories for a Product.
    - Takes the product ID as a path parameter and returns the category
        and its ancestor categories for that product.
    - Uses CategoryModelSerializer to serialize the category list.
    """

    serializer_class = CategoryModelSerializer
    model = Product

    def get_queryset(self):
        product_id: int = self.kwargs.get('id')
        product = self.model.objects.select_related('category').get(id=product_id)
        category = product.category
        return category.get_ancestors(include_self=True)


@extend_schema(tags=['Product Image', 'Product'])
class ProductImageModelViewSet(ModelViewSet):

    """
    ## Product Image Model Viewset
    - Handles CRUD operations for Product Images.


    Includes permissions to only allow admin users to create, update and delete
    product images while allowing read-only access to non-admin users.
    """

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageModelSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(tags=['Product Image', 'Product'])
class ProductImageListAPIView(ListAPIView):

    """
    ## List API View to retrieve Product Images for a Product.
    - Takes the product ID as a path parameter and returns all images
        for that product.
    - Uses ProductImageModelSerializer to serialize the image list.
    """

    model = Product
    serializer_class = ProductImageModelSerializer

    def get_queryset(self):
        product_id: int = self.kwargs.get('id')
        product = self.model.objects.prefetch_related('images').get(pk=product_id)
        return product.images.all()
