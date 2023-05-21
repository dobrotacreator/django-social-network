import datetime

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt

from users.models import User


class JWTAuthenticationMiddleware(BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            return None
        try:
            jwt_options = {
                'verify_signature': True,
                'verify_exp': True,
                'verify_nbf': False,
                'verify_iat': True,
                'verify_aud': False
            }
            payload = jwt.decode(auth_token, settings.SECRET_KEY,
                                 algorithms=['HS256', ], options=jwt_options)
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            return user, auth_token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Token is invalid')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

    @staticmethod
    def generate_token(user):
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
