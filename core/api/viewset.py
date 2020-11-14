import os
from urllib.request import urlopen

import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.api import serializers
from core import models
from . import integracao
from ..models import Publication
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializerGET
    instagram_integration = integracao.InstagramIntegration()

    def get_serializer_class(self):
        if self.action == 'generate_publication':
            return serializers.PublicationSerializerPOST
        return super().get_serializer_class()

    def get_media_temp(self, url):
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(url).read())
        img_temp.flush()
        return img_temp

    @action(detail=False, methods=['POST'], name="Generate Publication", url_name='generate-publication', url_path='generate')
    def generate_publication(self, request, *args, **kwargs):
        serializer = serializers.GeneratePublication(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_integracao = self.instagram_integration.html(request, url=serializer.data['url']).data

        publicacao_response = response_integracao['graphql'].get('shortcode_media')
        serializer = self.get_serializer(data=publicacao_response, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user, _ = User.objects.get_or_create(username=serializer.validated_data['autor'])
        publication = Publication.objects.filter(name=serializer.validated_data['name'], author=user,
                                                 cod_post__exact=serializer.validated_data['cod_post']).first()

        if not publication:
            publication = Publication(name=serializer.validated_data['name'], author=user,
                                      cod_post=serializer.validated_data['cod_post'])

            img_temp = self.get_media_temp(serializer.validated_data['image'])
            publication.image.save('post_%s.jpg' % serializer.validated_data['cod_post'], File(img_temp))
            publication.save()

        serializer = serializers.PublicationSerializerGET(instance=publication, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerialializer

