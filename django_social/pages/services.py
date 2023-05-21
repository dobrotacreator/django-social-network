from rest_framework.response import Response

from pages.models import Page
from tags.models import Tag
from users.models import User
from users.serializers import UserSerializer


# CREATE
def create_page_with_tags(request, serializer) -> Page:
    tag_names = extract_tag_names(request)
    page = create_page(serializer)

    if tag_names:
        tags = get_or_create_tags(tag_names)
        add_tags_to_page(page, tags)

    return page


def extract_tag_names(request) -> list[str]:
    tag_names = []
    if request.data.get('tags'):
        tag_names = [*request.data.pop('tags')]
    return tag_names


def create_page(serializer) -> Page:
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def get_or_create_tags(tag_names: list[str]) -> list[Tag]:
    tags = []
    for name in tag_names:
        tag, created = Tag.objects.get_or_create(name=name)
        tags.append(tag)
    return tags


def add_tags_to_page(page: Page, tags: list[Tag]) -> None:
    page.tags.set(tags)


# FOLLOW REQUESTS
def accept_follow_requests(page: Page) -> None:
    follow_requests = page.follow_requests.all()

    for follow_request in follow_requests:
        page.followers.add(follow_request)

    page.follow_requests.clear()


def accept_individual_follow_request(page: Page, user_id: int) -> Response | None:
    try:
        user: User = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'Invalid user id.'}, status=400)

    page.followers.add(user)
    page.follow_requests.remove(user)


def follow_requests_service(view, request, uuid: str = None) -> Response | None:
    page: Page = view.get_object()
    user_id: int | None = request.data.get('user_id')

    if user_id is None:
        accept_follow_requests(page)
        return Response({'detail': 'Follow requests accepted successfully.'}, status=200)
    else:
        return accept_individual_follow_request(page, user_id)


def reject_follow_requests(page: Page) -> None:
    page.follow_requests.clear()


def reject_individual_follow_request(page: Page, user_id: int) -> Response | None:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'Invalid user id.'}, status=400)

    page.follow_requests.remove(user)


def delete_follow_requests_service(view, request, uuid=None) -> Response | None:
    page: Page = view.get_object()
    user_id = request.data.get('user_id')

    if user_id is None:
        reject_follow_requests(page)
        return Response({'detail': 'Follow requests rejected successfully.'}, status=200)
    else:
        return reject_individual_follow_request(page, user_id)


def get_follow_requests(page: Page) -> dict:
    follow_requests = page.follow_requests.all()
    serializer = UserSerializer(follow_requests, many=True)
    return serializer.data


def get_follow_requests_service(view, request, uuid=None) -> Response:
    page: Page = view.get_object()
    follow_requests_data = get_follow_requests(page)
    return Response({'follow_requests': follow_requests_data}, status=200)


# BLOCK
def block_page(page: Page, end_date: str) -> None:
    page.block(end_date)


def block_page_service(view, request, uuid=None) -> Response:
    page: Page = view.get_object()
    end_date = request.data.get('end_date')
    block_page(page, end_date)
    return Response({'message': f'You have blocked this page on {end_date if end_date else "permanently"}.'},
                    status=200)


# UNBLOCK
def unblock_page(page: Page) -> None:
    page.unblock()


def delete_block_service(view, request, uuid=None) -> Response:
    page: Page = view.get_object()

    if page.is_blocked_now:
        unblock_page(page)
        return Response({'message': 'You have unblocked this page.'}, status=200)
    else:
        return Response({'message': 'There are no locks on this page anyway.'}, status=200)


# SUBSCRIBE
def subscribe_page(page: Page, user: User) -> dict:
    if not page.followers.filter(id=user.id).exists() and not page.follow_requests.filter(id=user.id).exists():
        if page.is_private:
            page.follow_requests.add(user)
            return {'message': 'You have sent a subscription request.'}
        else:
            page.followers.add(user)
            return {'message': 'You have subscribed to this page.'}
    elif page.followers.filter(id=user.id).exists():
        page.followers.remove(user)
        return {'message': 'You have unsubscribed from this page.'}
    elif page.follow_requests.filter(id=user.id).exists():
        page.follow_requests.remove(user)
        return {'message': 'You have canceled a subscription request.'}


def subscribe_page_service(view, request, uuid=None) -> Response:
    page: Page = view.get_object()
    user: User = request.user
    response_data = subscribe_page(page, user)
    return Response(response_data, status=200)
