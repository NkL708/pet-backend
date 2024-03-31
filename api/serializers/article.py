from rest_framework import serializers

from ..models.article import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "source_url", "short_text", "full_text"]
