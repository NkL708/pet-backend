from rest_framework import serializers

from ..models.digest import Digest
from ..serializers.article import ArticleSerializer


class DigestSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Digest
        fields = ["id", "title", "publication_date", "articles"]
