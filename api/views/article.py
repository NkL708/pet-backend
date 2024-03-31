from rest_framework import viewsets

from ..models.article import Article
from ..serializers.article import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
