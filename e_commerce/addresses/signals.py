from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from .models import ShippingAddress


@receiver(signal=post_save, sender=ShippingAddress)
def set_is_primary(sender, instance: ShippingAddress, **kwargs):
    if instance.is_primary:
        ShippingAddress.objects.filter(
            user=instance.user,
            is_primary=True
        ).exclude(
            id=instance.id
        ).update(
            is_primary=False
        )
