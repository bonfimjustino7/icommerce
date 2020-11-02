from django.urls import path, include
from rest_framework import routers

from core.api.viewset import PublicationViewSet

router = routers.DefaultRouter()
router.register(r'publication', PublicationViewSet)

urlpatterns = [
    path('', include(router.urls))
]
