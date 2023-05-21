from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    role = serializers.CharField(default='user')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'image_s3_path', 'role', 'title', 'is_blocked', 'blocked_until')
        extra_kwargs = {
            'password': {'write_only': True},
        }