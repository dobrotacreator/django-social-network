from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from searches.services import search_service
from users.permissions import IsNotBanned


class SearchViewSet(viewsets.GenericViewSet):
    serializer_class = None
    permission_classes = (IsAuthenticated, IsNotBanned)

    @action(detail=False, methods=['get'])
    def search(self, request):
        return search_service(self, request)
