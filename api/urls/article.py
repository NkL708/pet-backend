from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ..views.article import ArticleViewSet

router = DefaultRouter()
router.register(r"articles", ArticleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
