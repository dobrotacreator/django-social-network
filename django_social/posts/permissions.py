from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.page.owner == request.user


class CanViewPosts(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if obj.page.is_private:
                return obj.page.followers.filter(id=request.user.id).exists()
            return True


class CanInteractPosts(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.page.is_private:
            return obj.page.followers.filter(id=request.user.id).exists()
        return True
