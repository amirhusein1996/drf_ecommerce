from e_commerce.core.managers import SoftDeletationManager


class ProductManager(SoftDeletationManager):
    def get_queryset(self):
        return super().get_queryset().select_related('category', 'brand')
