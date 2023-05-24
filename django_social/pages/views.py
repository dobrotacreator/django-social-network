from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from aws.services import upload_image
from users.permissions import IsNotBanned, IsAdmin, IsModerator
from .models import Page
from .serializers import PageSerializer
from .permissions import CanViewPage, CanEditPage, IsOwnerOrReadOnly
from .services import create_page_with_tags, follow_requests_service, delete_follow_requests_service, \
    get_follow_requests_service, block_page_service, delete_block_service, subscribe_page_service


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (
        IsAuthenticated, IsNotBanned, IsAdmin | IsModerator | CanViewPage | CanEditPage)
    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        page = create_page_with_tags(request, serializer)
        self.perform_create(serializer)
        return self.get_success_response(page)

    def perform_create(self, serializer):
        upload_image(self.request, serializer, 'page_image', self.request.POST.get('uuid'))
        serializer.save()

    def get_success_response(self, page):
        serializer = self.get_serializer(page)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'],
            permission_classes=(IsAuthenticated, IsNotBanned, IsOwnerOrReadOnly))
    def follow_requests(self, request, uuid=None):
        return follow_requests_service(self, request, uuid)

    @follow_requests.mapping.delete
    def delete_follow_requests(self, request, uuid=None):
        return delete_follow_requests_service(self, request, uuid)

    @follow_requests.mapping.get
    def get_follow_requests(self, request, uuid=None):
        return get_follow_requests_service(self, request, uuid)

    @action(detail=True, methods=['post'],
            permission_classes=(IsAuthenticated, IsNotBanned, IsAdmin | IsModerator))
    def block(self, request, uuid=None):
        return block_page_service(self, request, uuid)

    @block.mapping.delete
    def delete_block(self, request, uuid=None):
        return delete_block_service(self, request, uuid)

    @action(detail=True, methods=['post'],
            permission_classes=(IsAuthenticated, IsNotBanned))
    def subscribe(self, request, uuid=None):
        return subscribe_page_service(self, request, uuid)
