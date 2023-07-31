from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'products'


router = DefaultRouter()
router.register(r'brands/', views.BrandModelViewSet)
router.register(r'categories/', views.CategoryModelViewSet)
router.register(r'products/', views.ProductModelViewSet)
router.register(r'images/', views.ProductImageModelViewSet)



brand_urls = [
    # path('brands/', views.BrandListView.as_view(), name='brand_list'),
    # path('brands/<int:pk>/', views.BrandDetailView.as_view(), name='brand_detail'),
    path('brands/<int:pk>/products/', views.BrandProductListView.as_view(), name='brand_products'),
]

category_urls = [
    # path('categories/', views.CategoryListView.as_view(), name='category_list'),
    # path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/products/', views.CategoryProductListView.as_view(), name='category_products'),
]

product_urls = [
    # path('products/', views.ProductListView.as_view(), name='product_list'),
    # path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/images/', views.ProductImageListView.as_view(), name='product_images'),
    path('products/<int:pk>/categories/', views.CategoryProduct.as_view(), name='product_categories'),
]

# image_urls = [
#     path('images/<int:pk>/', views.ProductImageDetailView.as_view(), name='productimage_detail'),
# ]

# urlpatterns: list = brand_urls + category_urls + product_urls + image_urls
urlpatterns: list = brand_urls + category_urls + product_urls + router.urls

