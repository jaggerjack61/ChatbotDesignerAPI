from rest_framework import routers
from api.views import UserViewSet

router = routers.SimpleRouter()
router.register(r'templates', UserViewSet)
urlpatterns = router.urls
