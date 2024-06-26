from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ..views.article import ArticleViewSet
from ..views.digest import DigestViewSet

router = DefaultRouter()
router.register(r"articles", ArticleViewSet)
router.register(r"digests", DigestViewSet)

urlpatterns = [path("", include(router.urls))]
