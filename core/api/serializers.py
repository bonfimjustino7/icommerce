from rest_framework import serializers
from core import models
from django.contrib.auth.models import User


class UserSerialializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')

class PublicationSerializer(serializers.ModelSerializer):
    author = UserSerialializer()
    id = serializers.CharField(read_only=True)

    class Meta:
        model = models.Publication
        fields = ('id', 'name','author', 'dt_criacao', 'dt_update')
