from django.urls import include, path
from rest_framework import routers

from .views import AOIAPIView

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"aoi", AOIAPIView, basename="aoi")

urlpatterns = [
    path("", include(router.urls)),
]
