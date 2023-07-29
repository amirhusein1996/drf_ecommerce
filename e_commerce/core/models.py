from django.db import models
from .managers import SoftDeletationManager
from django.utils import timezone


class SoftDeletation(models.Model):
    is_deleted = models.BooleanField(null=True, blank=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)


    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(
            update_fields=[
                'is_deleted',
                'deleted_at'
            ]
        )

    objects = SoftDeletationManager()