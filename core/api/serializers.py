from rest_framework import serializers
from core import models
from django.contrib.auth.models import User
from collections import OrderedDict
from ..utils import *

class UserSerialializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class PublicationSerializerGET(serializers.HyperlinkedModelSerializer):
    author = serializers.CharField()
    id = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='publication-detail')

    class Meta:
        model = models.Publication
        fields = ('id', 'cod_post', 'url', 'name', 'image', 'author', 'dt_criacao', 'dt_update')


class PublicationSerializerPOST(serializers.Serializer):
    autor = serializers.CharField()
    name = serializers.CharField(max_length=255)
    cod_post = serializers.CharField(max_length=50)
    image = serializers.URLField()

    def to_internal_value(self, data):
        res = OrderedDict()
        res['autor'] = data['owner']['username']
        res['image'] = data['display_resources'][0]['src'] if data['display_resources'] else None
        res['name'] = data['edge_media_to_caption']['edges'][0]['node']['text'] if data['edge_media_to_caption']['edges'] else None
        res['cod_post'] = data['shortcode']

        return res

    def validate(self, attrs):
        name_clean = clean_description(attrs.get('name'))
        attrs['name'] = name_clean
        return attrs



class ProductSerialializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail')
    publication = PublicationSerializerGET()

    class Meta:
        model = models.Product
        fields = ('id', 'url', 'publication', 'price', 'quantity_stock')


class GeneratePublication(serializers.Serializer):
    url = serializers.URLField()


class IntegracaoSerializer(serializers.Serializer):
    url = serializers.URLField()

    def validate(self, attrs):
        from urllib.parse import urlparse
        url = attrs.get('url')
        if url:
            parsed_url = urlparse(url)
            if not parsed_url.hostname == 'www.instagram.com':
                raise serializers.ValidationError({'error': 'URL inválida, a URL dever conter a origem www.instagram.com'})

        return attrs