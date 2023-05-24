from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from aws.services import upload_image
from .models import User
from .permissions import IsNotBanned, IsAdmin, IsModerator, IsOwnerOrReadOnly, IsOwner
from .serializers import UserSerializer
from .services import get_likes_service, block_user_service, unblock_user_service, authenticate_user_service, \
    logout_user_service, register_user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsNotBanned, IsAdmin | IsModerator | IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        upload_image(self.request, serializer, 'profile_image', self.request.user.id)
        serializer.save()

    @action(detail=True, methods=['get'],
            permission_classes=(IsAuthenticated, IsNotBanned, IsAdmin | IsOwner))
    def likes(self, request, pk=None):
        return get_likes_service(self, request, pk)

    @action(detail=True, methods=['post'],
            permission_classes=(IsAuthenticated, IsNotBanned, IsAdmin))
    def block(self, request, pk=None):
        return block_user_service(self, request, pk)

    @block.mapping.delete
    def delete_block(self, request, pk=None):
        return unblock_user_service(self, request, pk)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        return authenticate_user_service(request)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return logout_user_service()


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        return register_user(request)
