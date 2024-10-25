from rest_framework import serializers

from .models import Article, Digest


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "source_url", "short_text", "full_text"]


class DigestSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Digest
        fields = ["id", "title", "publication_date", "articles"]
