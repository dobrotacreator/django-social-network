from django.urls import path, include
from rest_framework import routers

from .views import NewsFeedViewSet

router = routers.SimpleRouter()
router.register(r'newsfeed', NewsFeedViewSet, basename='newsfeed')

urlpatterns = [
    path('', include(router.urls)),
]
