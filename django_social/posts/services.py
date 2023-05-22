from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .tasks import send_post_notification
from .models import Post
from pages.models import Page
from users.models import User
from users.serializers import UserSerializer


# GET QUERYSET
def get_page_by_uuid(page_uuid: str) -> Page | NotFound:
    try:
        page: Page = Page.objects.get(uuid=page_uuid)
        return page
    except Page.DoesNotExist:
        raise NotFound('A page with this uuid does not exist')


def get_posts_for_page(page: Page) -> tuple[Post]:
    return page.posts.all()


def get_posts_for_page_service(view) -> tuple[Post]:
    page_uuid: str = view.kwargs.get('pages_uuid')
    page: Page = get_page_by_uuid(page_uuid)
    posts: tuple[Post] = get_posts_for_page(page)
    return posts


# CREATE
def validate_reply_to(post_id: int) -> int | None:
    if post_id:
        try:
            post: Post = Post.objects.get(id=post_id)
            return post_id
        except Post.DoesNotExist:
            pass
    return None


def create_post_service(request):
    reply_to_id = request.data.get('reply_to')
    validated_reply_to_id = validate_reply_to(reply_to_id)

    if validated_reply_to_id:
        request.data['reply_to'] = validated_reply_to_id

    return request


# PERFORM CREATE
def perform_create_service(serializer) -> None:
    post: Post = serializer.instance

    page_uuid = post.page.uuid
    post_content = post.content

    send_post_notification.delay(page_uuid, post_content)


# LIKE
def toggle_like(post: Post, user: User) -> str:
    if user in post.liked_by.all():
        # User has already liked the post, so unlike it
        post.liked_by.remove(user)
        message = 'Post unliked successfully'
    else:
        # User hasn't liked the post, so like it
        post.liked_by.add(user)
        message = 'Post liked successfully'

    return message


def like_post_service(view, request, pages_uuid=None, pk=None) -> Response:
    post: Post = view.get_object()
    user: User = request.user
    message: str = toggle_like(post, user)
    return Response({'detail': message})


def get_likes(post: Post) -> dict:
    likes = post.liked_by
    serializer = UserSerializer(likes.all(), many=True)
    return serializer.data


def get_likes_service(view, request, pages_uuid=None, pk=None) -> Response:
    post: Post = view.get_object()
    likes_data: dict = get_likes(post)
    return Response({'likes': likes_data}, status=200)
