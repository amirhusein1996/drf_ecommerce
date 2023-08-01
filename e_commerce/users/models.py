from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
       A custom user model that extends Django's default user model.

       Attributes:
           email (str): The email address associated with the user account.
           _old_email (str): The previous email address associated with the user account.
                            This is used for tracking changes
                            to the user's email address so that appropriate actions can be taken,
                            such as sending a verification code.
           age (int): The age of the user.
           avatar (image): An image file representing the user's avatar.
                            This will be stored in the 'images/profiles' directory.

       Note:
           The `_old_email` field is used internally by the system and should not be modified directly.
       """

    email = models.EmailField(_("email address"), blank=True, unique=True)
    _old_email = models.EmailField(blank=True, null=True, editable=False)
    age = models.PositiveSmallIntegerField(verbose_name=_('age'), blank=True)
    avatar = models.ImageField(verbose_name=_('avatar'),upload_to='images/profiles', blank=True, null=True)
