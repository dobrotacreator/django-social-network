from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsNotBanned, IsAdmin, IsModerator
from users.serializers import UserSerializer
from pages.models import Page
from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwner, CanViewPosts, CanInteractPosts


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsNotBanned, IsAdmin | IsModerator | IsOwner | CanViewPosts)

    def get_queryset(self):
        page_uuid = self.kwargs.get('pages_uuid')
        try:
            page = Page.objects.get(uuid=page_uuid)
        except Page.DoesNotExist:
            raise NotFound('A page with this uuid does not exist')
        return page.posts

    def create(self, request, *args, **kwargs):
        reply_to_id = request.data.get('reply_to')
        if reply_to_id:
            if Post.objects.get(id=reply_to_id):
                request.data['reply_to'] = reply_to_id

        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated, IsNotBanned, IsAdmin | IsModerator | IsOwner | CanInteractPosts])
    def like(self, request, pages_uuid=None, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.liked_by.all():
            # User has already liked the post, so unlike it
            post.liked_by.remove(user)
            message = 'Post unliked successfully'
        else:
            # User hasn't liked the post, so like it
            post.liked_by.add(user)
            message = 'Post liked successfully'

        return Response({'detail': message})

    @like.mapping.get
    def get_likes(self, request, pages_uuid=None, pk=None):
        post: Post = self.get_object()
        likes = post.liked_by
        serializer = UserSerializer(likes.all(), many=True)
        return Response({'likes': serializer.data}, status=200)
