from rest_framework import viewsets

from core.api.serializers import PublicationSerializer
from core.models import Publication


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
