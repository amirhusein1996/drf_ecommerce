from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from e_commerce.core.models import SoftDeletation
from .managers import ProductManager


class Brand(SoftDeletation):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    description = models.TextField()
    slug = models.SlugField(verbose_name=_('slug'), max_length=255, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(SoftDeletation, MPTTModel):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    description = models.TextField(verbose_name=_('description'))
    parent = TreeForeignKey(verbose_name=_('parent'), to='self', on_delete=models.PROTECT,
                            related_name=_('children'), blank=True, null=True)
    slug = models.SlugField(verbose_name=_('slug'), max_length=255, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(SoftDeletation):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    short_description = models.CharField(verbose_name=_('short description'), max_length=500)
    description = models.TextField(verbose_name=_('description'), blank=True)
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=2)
    main_image = models.ImageField(verbose_name=_('main image'), upload_to='images/products/main/',
                                   blank=True, null=True)
    brand = models.ForeignKey(verbose_name=_('brand'), to=Brand, on_delete=models.PROTECT, related_name='products')
    category = TreeForeignKey(verbose_name=_('categories'), to=Category, related_name='products',
                              on_delete=models.PROTECT)
    slug = models.SlugField(verbose_name=_('slug'), max_length=255, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    objects = ProductManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(SoftDeletation):
    image = models.ImageField(verbose_name=_('image'), upload_to='images/products/', blank=True, null=True)
    product = models.ForeignKey(verbose_name=_('product'), to=Product, null=True, on_delete=models.CASCADE,
                                related_name='images')

    class Meta:
        verbose_name = _('ProductImage')
        verbose_name_plural = _('ProductImages')
