from django.db.models import Q
from rest_framework.response import Response

from pages.models import Page
from users.models import User


def search_users(query) -> list[dict]:
    users: tuple[User] = User.objects.filter(Q(title__icontains=query) | Q(username__icontains=query))
    users_data: list[dict] = [{'title': user.title, 'username': user.username} for user in users]
    return users_data


def search_pages(query: str) -> list[dict]:
    pages: tuple[Page] = Page.objects.filter(
        Q(name__icontains=query) | Q(uuid__icontains=query) | Q(tags__name__icontains=query)
    )
    pages_data: list[dict] = [
        {'name': page.name, 'uuid': page.uuid, 'tags': list(page.tags.values_list('name', flat=True))}
        for page in pages
    ]
    return pages_data


def search_service(view, request) -> Response:
    query: str = request.query_params.get('q', None)
    if not query:
        return Response([])

    users_data = search_users(query)
    pages_data = search_pages(query)

    return Response({
        'users': users_data,
        'pages': pages_data
    })
