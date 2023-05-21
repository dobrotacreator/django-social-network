from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsNotBanned, IsAdmin, IsModerator
from .serializers import PostSerializer
from .permissions import IsOwner, CanViewPosts, CanInteractPosts
from .services import get_posts_for_page_service, create_post_service, like_post_service, get_likes_service


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsNotBanned, IsAdmin | IsModerator | IsOwner | CanViewPosts)

    def get_queryset(self):
        return get_posts_for_page_service(self)

    def create(self, request, *args, **kwargs):
        return create_post_service(self, request, *args, **kwargs)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated, IsNotBanned, IsAdmin | IsModerator | IsOwner | CanInteractPosts])
    def like(self, request, pages_uuid=None, pk=None):
        return like_post_service(self, request, pages_uuid, pk)

    @like.mapping.get
    def get_likes(self, request, pages_uuid=None, pk=None):
        return get_likes_service(self, request, pages_uuid=None, pk=None)
