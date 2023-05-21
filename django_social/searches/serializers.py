from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    page_id = serializers.IntegerField(source='id', required=False)
    page_name = serializers.CharField(source='name', required=False)
    user_id = serializers.IntegerField(source='id', required=False)
    user_title = serializers.CharField(source='title', required=False)
    user_username = serializers.CharField(source='username', required=False)
