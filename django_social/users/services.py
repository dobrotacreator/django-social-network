from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from django_social.middleware import JWTAuthenticationMiddleware
from posts.models import Post
from posts.serializers import PostSerializer
from users.models import User


# LIKES
def get_liked_posts(user) -> dict:
    likes: Post = user.liked_posts.all()
    serializer = PostSerializer(likes, many=True)
    return serializer.data


def get_likes_service(view, request, pk=None) -> Response:
    user = view.get_object()
    liked_posts = get_liked_posts(user)
    return Response({'liked_posts': liked_posts}, status=200)


# BLOCK
def block_user(user: User, end_date: str) -> dict:
    user.block(end_date)
    return {'message': f'You have blocked this user and their pages on {end_date if end_date else "permanently"}.'}


def block_user_service(view, request, pk=None) -> Response:
    user: User = view.get_object()
    end_date: str = request.data.get('end_date')
    response_data = block_user(user, end_date)
    return Response(response_data, status=200)


def unblock_user(user: User) -> dict:
    user.unblock()
    return {'message': 'You have unblocked this user.'}


def unblock_user_service(view, request, pk=None) -> Response:
    user: User = view.get_object()
    if user.is_blocked_now:
        response_data: dict = unblock_user(user)
        return Response(response_data, status=200)
    return Response({'message': 'There are no locks on this user anyway.'}, status=200)


# LOGIN
# POST
def authenticate_user(username: str, password: str) -> dict:
    user = authenticate(username=username, password=password)
    if user:
        token = JWTAuthenticationMiddleware.generate_token(user)
        return {'token': token}
    else:
        return {'error': 'Invalid credentials'}


def authenticate_user_service(request) -> Response:
    username: str = request.data.get('username')
    password: str = request.data.get('password')
    response_data: dict = authenticate_user(username, password)
    status_code = status.HTTP_200_OK if 'token' in response_data else status.HTTP_401_UNAUTHORIZED
    return Response(response_data, status=status_code)


# LOGOUT
# POST
def logout_user_service():
    response = Response({'success': 'Successfully logged out'})
    response.delete_cookie('jwt')
    return response


# REGISTER
# POST
def register_user_service(username: str, password: str, email: str) -> Response:
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


def register_user(request) -> Response:
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    return register_user_service(username, password, email)
