from django.contrib.gis.geos import GEOSGeometry
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from geo_platform.apps.aoi.models import AOI
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class AOISerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AOI
        geo_field = "geometry"
        fields = (
            "pk",
            "geometry_id",
            "geometry",
            "region",
            "crop",
            "productivity",
            "area_ha",
            "user",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "pk",
            "created_at",
            "updated_at",
        )


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "analytics",
            request_only=True,
            value={
                "region": "FR-22",
            },
        ),
        OpenApiExample(
            "analytics",
            response_only=True,
            value={"total_area": 0.0, "total_yield": 0.0, "average_yield": 0.0},
        ),
    ]
)
class AnalyticsSerializer(serializers.Serializer):
    region = serializers.CharField(min_length=4, max_length=5)


class IntersectionSerializer(serializers.Serializer):
    geometry = serializers.CharField(min_length=1, max_length=1000)

    def validate_geometry(self, value) -> GEOSGeometry:
        try:
            geometry = GEOSGeometry(value)
        except Exception as e:
            raise serializers.ValidationError from e
        return geometry
