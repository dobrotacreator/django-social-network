from rest_framework import serializers

from .models import Page
from tags.serializers import TagSerializer


class PageSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    owner = serializers.CharField(default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True, required=False)
    image = serializers.ReadOnlyField()

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'followers', 'image', 'is_private',
                  'follow_requests', 'is_blocked', 'blocked_until')
