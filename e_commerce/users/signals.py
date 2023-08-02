from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver


User = get_user_model()


@receiver(signal=pre_save, sender=User)
def verify_email(instance: User, **kwargs):
    if instance.email and (instance.email != instance.old_email):
        # todo:Send verification email to the new email address
        pass

    # Update the old email address field
    instance._old_email = instance.email

