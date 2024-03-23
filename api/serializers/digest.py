from rest_framework import serializers

from ..models.digest import Digest


class DigestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Digest
        fields = ["id", "title", "publication_date", "articles"]
