from django.db.models import Manager, QuerySet
from django.utils import timezone


class SoftDeletationQuerySet(QuerySet):
    def delete(self):
        return self.update(
            is_deleted=True,
            deleted_at=timezone.now()
        )


class SoftDeletationManager(Manager):
    def get_queryset(self):
        return SoftDeletationQuerySet(
            model=self.model,
            using=self._db
        ).exclude(
            is_deleted=True
        )
