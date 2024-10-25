from rest_framework import viewsets

from .models import Article, Digest
from .serializers import ArticleSerializer, DigestSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class DigestViewSet(viewsets.ModelViewSet):
    queryset = Digest.objects.all()
    serializer_class = DigestSerializer
