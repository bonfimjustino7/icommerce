from . import integracao
from django.urls import path, include
from rest_framework import routers

from core.api import viewset


router = routers.DefaultRouter()
router.register(r'publication', viewset.PublicationViewSet, base_name='publication')
router.register(r'product', viewset.ProductViewSet, base_name='product')
router.register(r'instagram', integracao.InstagramIntegration, base_name='instagram')

urlpatterns = [
    path('', include(router.urls))
]
