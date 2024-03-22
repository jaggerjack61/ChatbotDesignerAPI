from django.urls import path, include
from rest_framework import routers
from .views import TemplateViewSet, TemplatePageViewSet, TemplateOptionViewSet

router = routers.SimpleRouter()
router.register(r'templates', TemplateViewSet)
router.register(r'template-pages', TemplatePageViewSet)
router.register(r'template-options', TemplateOptionViewSet)

urlpatterns = router.urls

