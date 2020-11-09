import requests
from django.contrib.auth.models import User
from django.http import QueryDict
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.api import serializers
from core import models
from bs4 import BeautifulSoup
from . import integracao
from ..models import Publication
from ..utils import get_value_graph


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    instagram_integration = integracao.InstagramIntegration()

    @action(detail=False, methods=['POST'], name="Generate Publication", url_name='generate-publication', url_path='generate')
    def generate_publication(self, request, *args, **kwargs):
        serializer = serializers.GeneratePublication(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_integracao = self.instagram_integration.html(request, url=serializer.data['url']).data

        descricao = get_value_graph(response_integracao.get('graphql'), 'accessibility_caption')
        img = get_value_graph(response_integracao.get('graphql'), 'display_url')
        autor = get_value_graph(response_integracao.get('graphql'), 'username')

        user, _ = User.objects.get_or_create(username=autor)
        publication = Publication.objects.create(name=descricao, url_image=img, author=user)
        serializer = serializers.PublicationSerializer(instance=publication, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerialializer

