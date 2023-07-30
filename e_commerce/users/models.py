from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, unique=True)
    age = models.PositiveSmallIntegerField(verbose_name=_('age'), blank=True)
    avatar = models.ImageField(verbose_name=_('avatar'),upload_to='images/profiles', blank=True, null=True)
