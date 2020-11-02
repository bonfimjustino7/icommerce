from django.urls import path, include
from rest_framework import routers

from core.api import viewset

router = routers.DefaultRouter()
router.register(r'publication', viewset.PublicationViewSet, base_name='publication')
router.register(r'product', viewset.ProductViewSet, base_name='product')

urlpatterns = [
    path('', include(router.urls))
]
