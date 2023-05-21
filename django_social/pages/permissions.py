from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

from .models import Page


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class IsSubscriber(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if user is the subscriber
        if obj.followers.filter(id=request.user.id).exists():
            return True
        raise PermissionDenied('You are not a subscriber of this page.')


class CanEditPage(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and obj.owner == request.user:
            # Regular users can edit title and description fields only
            editable_fields = ['name', 'uuid', 'description', 'tags', 'image', 'is_private']
            if not set(editable_fields).issuperset(request.data.keys()):
                raise PermissionDenied(f'You can only edit these parameters: {editable_fields}.')
            return True
        else:
            return False


class CanViewPage(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.is_private or request.user.follows.filter(uuid=obj.uuid).exists():
            return True
        else:
            raise PermissionDenied('This page is private. Please subscribe to view.')
