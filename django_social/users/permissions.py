from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "admin"


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "moderator"


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to create, update, or delete objects
    """

    def has_permission(self, request, view):
        # Allow read-only access for all users
        if request.method in SAFE_METHODS:
            return True

        # Only allow admin users to create, update, or delete objects
        return request.user and request.user.role == "admin"


class IsModeratorOrReadOnly(BasePermission):
    """
    Custom permission to only allow moderator users to create, update, or delete objects
    """

    def has_permission(self, request, view):
        # Allow read-only access for all users
        if request.method in SAFE_METHODS:
            return True

        # Only allow admin users to create, update, or delete objects
        return request.user and request.user.role == "moderator"


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.id == request.user.id


class IsNotBanned(BasePermission):
    """
    Allows access only to non-banned users.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_blocked_now:
            return True
        return False
