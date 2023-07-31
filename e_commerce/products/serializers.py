from rest_framework import serializers
from .models import (
    Product,
    ProductImage,
    Brand,
    Category,
)


class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'description', 'slug')
        read_only_fields = ('id', 'slug')


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'slug', 'parent')
        read_only_fields = ('id', 'slug')
        write_only_fields = ('parent',)


class ProductImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'product')
        read_only_fields = ('id',)
        write_only_fields = ('product',)


class ProductDetailModelSerializer(serializers.ModelSerializer):
    brand = BrandModelSerializer()
    category = CategoryModelSerializer()
    categories = serializers.SerializerMethodField()
    images = ProductImageModelSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'categories')

    def get_categories(self, obj: Product):
        serializer = CategoryModelSerializer(
            obj.category.get_ancestors(include_self=True),
            many=True
        )
        return serializer.data


class ProductListModelSerializer(serializers.ModelSerializer):
    brand = BrandModelSerializer()
    category = CategoryModelSerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'short_description', 'price', 'main_image', 'brand', 'category', 'slug')
