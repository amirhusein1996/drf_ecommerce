from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from e_commerce.products.models import Product, Category


class Coupon(models.Model):
    COUPON_TYPE = (
        ('fixed', _('Fixed amount')),
        ('percent', _('Percent discounted'))
    )

    code = models.CharField(verbose_name=_('coupon code'), max_length=50, unique=True)
    valid_from = models.DateTimeField(verbose_name=_('valid from'))
    valid_to = models.DateTimeField(verbose_name=_('valid to'))
    amount = models.DecimalField(verbose_name=_('amount'), max_digits=10, decimal_places=2)
    type = models.CharField(verbose_name=_('coupon type'), choices=COUPON_TYPE, max_length=10)
    percent_off = models.IntegerField(verbose_name=_('percent off'), help_text='Percent off (1~100)', null=True,
                                      blank=True)
    is_active = models.BooleanField(verbose_name=_('active'), )
    max_use = models.IntegerField(verbose_name=_('max use'), help_text=_('Maximum number of uses for this coupon'),
                                  default=0)
    products = models.ManyToManyField(verbose_name=_('products'), to=Product, blank=True)
    categories = models.ManyToManyField(verbose_name=_('categories'), to=Category, blank=True)
    num_uses = models.IntegerField(verbose_name=_('uses number'), help_text=_('number of times coupon has been used'),
                                   default=0)

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')

    def is_valid(self, order):
        now = timezone.now()
        if now < self.valid_from or now > self.valid_to:
            return False

        if self.max_use and self.num_uses >= self.max_use:
            return False

        if self.products.exists() and not self.products.filter(
                id__in=order.items.values_list('product_id')
        ).exists():
            return False

        if self.categories.exists() and not self.categories.filter(
                id__in=order.items.values_list('product__category_id')
        ).exists():
            return False

        return True
