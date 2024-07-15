from rest_framework.routers import DefaultRouter

from posts.api.views import PostViewSet, CommentViewSet


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = router.urls
