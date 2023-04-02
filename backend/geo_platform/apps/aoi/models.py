from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import MultiPolygonField
from django.db import models


class AOI(models.Model):
    geometry_id = models.PositiveIntegerField()
    crop = models.TextField(max_length=120, blank=True, null=False)
    productivity = models.FloatField(null=True)
    region = models.TextField(max_length=100, blank=True)
    area_ha = models.FloatField(null=True)
    geometry = MultiPolygonField(spatial_index=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def filter_field(self) -> str:
        return "geometry"

    def __str__(self) -> str:
        return str(self.geometry_id)
