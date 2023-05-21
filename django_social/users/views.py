from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from django_social.middleware import JWTAuthenticationMiddleware
from posts.serializers import PostSerializer
from .models import User
from .permissions import IsNotBanned, IsAdmin, IsModerator, IsOwnerOrReadOnly
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsNotBanned, IsAdmin | IsModerator | IsOwnerOrReadOnly)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        user: User = self.get_object()
        likes = user.liked_posts
        serializer = PostSerializer(likes.all(), many=True)
        return Response({'liked_posts': serializer.data}, status=200)

    @action(detail=True, methods=['post'],
            permission_classes=(IsAuthenticated, IsNotBanned, IsAdmin))
    def block(self, request, pk=None):
        user: User = self.get_object()
        end_date = request.data.get('end_date')
        user.block(end_date)
        return Response(
            {'message': f'You have blocked this user and his pages on {end_date if end_date else "permanently"}.'},
            status=200)

    @block.mapping.delete
    def delete_block(self, request, pk=None):
        user: User = self.get_object()
        if user.is_blocked_now:
            user.unblock()
            return Response({'message': 'You have unblocked this page.'}, status=200)
        return Response({'message': 'There are no locks on this page anyway.'}, status=200)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token = JWTAuthenticationMiddleware.generate_token(user)
            return Response({'token': token})
        else:
            return Response({'error': 'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Delete the token from the client-side
        response = Response({'success': 'Successfully logged out'})
        response.delete_cookie('jwt')
        return response


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not (username and password and email):
            return Response({'error': 'Missing required fields'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            return Response({'error': 'User already exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        token = JWTAuthenticationMiddleware.generate_token(user)
        return Response({'token': token})
