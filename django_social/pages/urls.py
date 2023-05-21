from django.urls import path, include
from rest_framework_nested import routers

from .views import PageViewSet
from posts.views import PostViewSet

router = routers.SimpleRouter()
router.register('pages', PageViewSet)

posts_router = routers.NestedSimpleRouter(
    router,
    r'pages',
    lookup='pages')

posts_router.register(
    r'posts',
    PostViewSet,
    basename='pages-posts')

app_name = 'pages'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
]
