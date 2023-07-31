from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow account admins to modify the object,
    but allow anyone to view it.
    """

    def has_permission(self, request, view):
        # Allow read-only access for safe methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Only allow account admins to modify the object
        return request.user.is_authenticated and request.user.is_superuser
