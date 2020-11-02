from rest_framework import viewsets

from core.api import serializers
from core import models


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerialializer
