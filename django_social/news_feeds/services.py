from rest_framework.response import Response

from pages.models import Page
from posts.models import Post
from posts.serializers import PostSerializer


def get_user_subscribed_pages(user) -> tuple[Page]:
    return user.follows.all()


def get_feed_posts(subscribed_pages) -> tuple[Post]:
    posts = Post.objects.filter(page__in=subscribed_pages).order_by('-created_at')
    return posts


def get_feed_service(view, request) -> Response:
    subscribed_pages = get_user_subscribed_pages(request.user)
    posts = get_feed_posts(subscribed_pages)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
