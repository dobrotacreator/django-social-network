from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsNotBanned
from users.models import User
from users.serializers import UserSerializer
from pages.models import Page
from pages.serializers import PageSerializer


class SearchViewSet(viewsets.GenericViewSet):
    serializer_class = None
    permission_classes = (IsAuthenticated, IsNotBanned)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', None)
        if not query:
            return Response([])

        # Search for users and pages by query
        users = User.objects.filter(Q(title__icontains=query) | Q(username__icontains=query))
        pages = Page.objects.filter(
            Q(name__icontains=query) | Q(uuid__icontains=query) | Q(tags__name__icontains=query))

        pages_data = [{'name': page.name, 'uuid': page.uuid, 'tags': list(page.tags.values_list('name', flat=True))}
                      for page in pages]
        users_data = [{'title': user.title, 'username': user.username}
                      for user in users]

        return Response({
            'users': users_data,
            'pages': pages_data
        })
