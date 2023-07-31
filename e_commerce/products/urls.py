from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'products'


router = DefaultRouter()
router.register(r'brands', views.BrandModelViewSet)
router.register(r'categories', views.CategoryModelViewSet)
router.register(r'products', views.ProductModelViewSet)
router.register(r'images', views.ProductImageModelViewSet)


brand_urls = [
    path('brands/<int:pk>/products/', views.BrandProductListAPIView.as_view(), name='brand_products'),
]

category_urls = [
    path('categories/<int:pk>/products/', views.CategoryProductListAPIView.as_view(), name='category_products'),
]

product_urls = [
    path('products/<int:pk>/images/', views.ProductImageListAPIView.as_view(), name='product_images'),
    path('products/<int:pk>/categories/', views.CategoryProductListAPIView.as_view(), name='product_categories'),
]

urlpatterns: list = brand_urls + category_urls + product_urls + router.urls

