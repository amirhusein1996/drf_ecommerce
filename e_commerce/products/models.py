from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from e_commerce.core.models import SoftDeletation


class Brand(SoftDeletation):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return self.name


class Category(SoftDeletation, MPTTModel):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    description = models.TextField(verbose_name=_('description'))
    parent = TreeForeignKey(verbose_name=_('parent'), to='self', on_delete=models.PROTECT,
                            related_name=_('children'), blank=True, null=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Product(SoftDeletation):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    description = models.TextField(verbose_name=_('description'), blank=True)
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=2)
    brand = models.ForeignKey(verbose_name=_('brand'), to=Brand, on_delete=models.PROTECT)
    categories = TreeManyToManyField(verbose_name=_('categories'), to=Category, related_name='products')

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name


class ProductImage(SoftDeletation):
    image = models.ImageField(verbose_name=_('amount'), upload_to='images/products/', blank=True, null=True)
    product = models.ForeignKey(verbose_name=_('product'), to=Product, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('ProductImage')
        verbose_name_plural = _('ProductImages')
