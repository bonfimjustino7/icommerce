import requests
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class InstagramIntegration(GenericViewSet):

    @action(detail=False, methods=['GET'], name='Publication HTML', url_path='page', url_name='page')
    def html(self, request, *args, **kwargs):
        url_publication = request.query_params.get('url') or kwargs.get('url')

        response = requests.get(url_publication, params={
            '__a': 1
        })

        return Response(response.json())
