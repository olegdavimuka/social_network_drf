from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission that grants all permissions
    to superusers and staff users
    and only read permissions to regular users.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission that grants all object permissions
    to superusers, staff users and owners
    and only read permissions to regular users.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user


class IsOwnerOrRestricted(permissions.BasePermission):
    """
    Custom permission that grants all object permissions
    to superusers, staff users and owners
    and no permissions to regular users.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.user.is_staff:
            return True

        return obj == request.user


class IsNotAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow unauthenticated users to access the API.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return False
