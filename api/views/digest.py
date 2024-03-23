from rest_framework import viewsets

from ..models.digest import Digest
from ..serializers.digest import DigestSerializer


class DigestViewSet(viewsets.ModelViewSet):
    queryset = Digest.objects.all()
    serializer_class = DigestSerializer
