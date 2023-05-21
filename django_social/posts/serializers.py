from rest_framework import serializers

from pages.serializers import PageSerializer
from pages.models import Page
from users.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    page = PageSerializer(required=False, read_only=True)
    replies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'reply_to', 'replies', 'created_at', 'updated_at')

    def create(self, validated_data):
        page_uuid = self.context['view'].kwargs.get('pages_uuid')  # Retrieve the 'page_uuid' from the URL parameters
        page = Page.objects.get(uuid=page_uuid)  # Retrieve the Page object based on the 'page_uuid'

        validated_data['page'] = page  # Set the 'page' field in the validated data to the retrieved Page object

        post = super().create(validated_data)

        return post
