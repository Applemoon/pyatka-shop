from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ItemViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryViewSet)
router.register(r'items', ItemViewSet)

urlpatterns = router.urls
