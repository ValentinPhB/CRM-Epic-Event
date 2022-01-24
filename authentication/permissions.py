from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Allows access to SAFE_METHODS only to non-admin users or other groups than "GESTION" one.
    """

    def has_permission(self, request, view):
        return bool(
            request.user.is_staff
            or request.user.is_superuser
            or request.user.group == "GESTION"
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_staff
            or request.user.is_superuser
            or request.user.group == "GESTION"
        )
