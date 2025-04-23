from rest_framework.routers import DefaultRouter
from .views import ServerViewSet

router = DefaultRouter()
router.register(r'servers', ServerViewSet)

urlpatterns = router.urls
