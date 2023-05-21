from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from users.permissions import IsNotBanned, IsAdmin, IsModerator
from tags.models import Tag
from users.serializers import UserSerializer
from .models import Page
from .serializers import PageSerializer
from .permissions import CanViewPage, CanEditPage, IsOwnerOrReadOnly


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (
        IsAuthenticated, IsNotBanned, IsAdmin | IsModerator | CanViewPage | CanEditPage)
    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        # Get the tags from the request data
        tag_names = []
        if request.data.get('tags'):
            tag_names = [*request.data.pop('tags')]

        # Create the page object
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = serializer.save()

        # Create new tags or get existing tags
        if tag_names:
            tags = []
            for name in list(tag_names):
                tag, created = Tag.objects.get_or_create(name=name)
                tags.append(tag)

            # Add the tags to the page
            page.tags.set(tags)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'],
            permission_classes=(IsAuthenticated, IsNotBanned, IsOwnerOrReadOnly))
    def follow_requests(self, request, uuid=None):
        page: Page = self.get_object()

        follow_requests = page.follow_requests
        user_id = request.data.get('user_id')

        if user_id is None:
            for follow_request in follow_requests.all():
                page.followers.add(follow_request)
            follow_requests.clear()
            return Response({'detail': 'Follow requests accepted successfully.'}, status=200)
        else:
            user = User.objects.get(id=user_id)
            if user:
                page.followers.add(user)
                page.follow_requests.remove(user)
                return Response({'detail': 'Follow request accepted.'}, status=200)
            return Response({'detail': 'Invalid user id.'}, status=400)

    @follow_requests.mapping.delete
    def delete_follow_requests(self, request, uuid=None):
        page: Page = self.get_object()

        follow_requests = page.follow_requests
        user_id = request.data.get('user_id')

        if user_id is None:
            follow_requests.clear()
            return Response({'detail': 'Follow requests rejected successfully.'}, status=200)
        else:
            user = User.objects.get(id=user_id)
            if user:
                page.follow_requests.remove(user)
                return Response({'detail': 'Follow request rejected.'}, status=200)

    @follow_requests.mapping.get
    def get_follow_requests(self, request, uuid=None):
        page: Page = self.get_object()
        follow_requests = page.follow_requests
        serializer = UserSerializer(follow_requests.all(), many=True)
        return Response({'follow_requests': serializer.data}, status=200)

    @action(detail=True, methods=['post'],
            permission_classes=(IsAuthenticated, IsNotBanned, IsAdmin | IsModerator))
    def block(self, request, uuid=None):
        page = self.get_object()
        end_date = request.data.get('end_date')
        page.block(end_date)
        return Response({'message': f'You have blocked this page on {end_date if end_date else "permanently"}.'},
                        status=200)

    @block.mapping.delete
    def delete_block(self, request, uuid=None):
        page = self.get_object()
        if page.is_blocked_now:
            page.unblock()
            return Response({'message': 'You have unblocked this page.'}, status=200)
        return Response({'message': 'There are no locks on this page anyway.'}, status=200)

    @action(detail=True, methods=['post'],
            permission_classes=(IsAuthenticated, IsNotBanned))
    def subscribe(self, request, uuid=None):
        page: Page = self.get_object()
        user: User = request.user
        if not page.followers.filter(id=user.id).exists() and not page.follow_requests.filter(id=user.id).exists():
            if page.is_private:
                page.follow_requests.add(user)
                return Response({'message': 'You have sent a subscription request.'}, status=200)
            page.followers.add(user)
            return Response({'message': 'You have subscribed to this page.'}, status=200)
        elif page.followers.filter(id=user.id).exists():
            page.followers.remove(user)
            return Response({'message': 'You have unsubscribed from this page.'}, status=200)
        elif page.follow_requests.filter(id=user.id).exists():
            page.follow_requests.remove(user)
            return Response({'message': 'You have canceled a subscription request.'}, status=200)
