from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from e_commerce.coupon.models import Coupon
from e_commerce.addresses.models import BillingAddress, ShippingAddress
from e_commerce.products.models import Product

User = get_user_model()


class Order(models.Model):
    # Order status choices
    ORDER_STATUS = (
        ('open', _('Open')),
        ('paid', _('Paid')),
        ('shipped', _('Shipped')),
        ('refunded', _('Refunded')),
    )

    user = models.ForeignKey(verbose_name=_('user'), to=User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(verbose_name=_('coupon'), to=Coupon, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_st = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)
    is_paid = models.BooleanField(verbose_name=_('paid'), default=False)
    is_shipped = models.BooleanField(verbose_name=_('shipped'), default=False)
    is_refunded = models.BooleanField(verbose_name=_('refunded'), default=False)
    billed_to = models.ForeignKey(verbose_name=_('billed to'),
                                  to=BillingAddress, on_delete=models.SET_NULL, null=True)
    shipped_to = models.ForeignKey(verbose_name=_('shipped to'),
                                   to=ShippingAddress, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(verbose_name=_('comment'), blank=True)
    status = models.CharField(verbose_name=_('order status'), max_length=120, choices=ORDER_STATUS)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Order')
        verbose_name_plural = _("Orders")

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total = Decimal(0)
        for item in self.orderitem_set.all():
            total += item.get_cost()

        if self.coupon:
            valid = self.coupon.is_valid(self)
            if valid:
                if self.coupon.type == 'fixed':
                    total -= self.coupon.amount
                if self.coupon.type == 'percent':
                    total -= total * (self.coupon.percent_off / Decimal(100))

        return total


class OrderItem(models.Model):
    order = models.ForeignKey(verbose_name=_('order'), to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(verbose_name=_('product'), to=Product, on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=2)
    quantity = models.IntegerField(verbose_name=_('quantity'), default=1)

    class Meta:
        verbose_name = _('user'),
        verbose_name_plural = _('users')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
