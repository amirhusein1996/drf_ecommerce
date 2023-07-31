from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


User = get_user_model()


class Address(models.Model):
    user = models.ForeignKey(verbose_name=_('user'), to=User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name=_('first name'), max_length=30)
    last_name = models.CharField(verbose_name=_('last name'), max_length=30)
    phone = PhoneNumberField(verbose_name=_('phone number'), )
    street = models.CharField(verbose_name=_('street address'), max_length=200)
    city = models.CharField(verbose_name=_('city'), max_length=100)
    zip_code = models.CharField(verbose_name=_('zip code'), max_length=20)
    state = models.CharField(verbose_name=_('state'), max_length=50)
    country = CountryField(verbose_name=_('country'))


    class Meta:
        abstract = True
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class BillingAddress(Address):
    email = models.EmailField()

    class Meta:
        verbose_name = _('Billing Address')
        verbose_name_plural = _('Billing Addresses')


class ShippingAddress(Address):
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Shipping Address')
        verbose_name_plural = _('Shipping Addresses')
