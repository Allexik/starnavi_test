from rest_framework.routers import DefaultRouter

from accounts.api.views import ProfileViewSet


router = DefaultRouter()
router.register('profiles', ProfileViewSet)

urlpatterns = router.urls
