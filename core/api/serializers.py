from rest_framework import serializers
from core import models
from django.contrib.auth.models import User


class UserSerialializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class PublicationSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerialializer()
    id = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='publication-detail')

    class Meta:
        model = models.Publication
        fields = ('id', 'url', 'name','author', 'dt_criacao', 'dt_update')


class ProductSerialializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail')
    publication = PublicationSerializer()

    class Meta:
        model = models.Product
        fields = ('id', 'url', 'publication', 'price', 'quantity_stock')