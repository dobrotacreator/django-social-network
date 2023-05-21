from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from news_feeds.services import get_feed_service
from posts.models import Post
from users.permissions import IsNotBanned
from posts.serializers import PostSerializer


class NewsFeedViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated, IsNotBanned))
    def feed(self, request):
        return get_feed_service(self, request)
