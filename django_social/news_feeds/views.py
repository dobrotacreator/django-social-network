from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from users.permissions import IsNotBanned
from posts.serializers import PostSerializer


class NewsFeedViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated, IsNotBanned))
    def feed(self, request):
        subscribed_pages = request.user.follows.all()
        posts: Post = Post.objects.filter(page__in=subscribed_pages).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
