from django.db.models import Sum
from django.db.models.functions import Round
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   OpenApiResponse, extend_schema,
                                   extend_schema_view)
from geo_platform.apps.aoi.filters import _DistanceToPointOrderingFilter
from geo_platform.apps.aoi.models import AOI
from geo_platform.apps.aoi.serializers import (AnalyticsSerializer,
                                               AOISerializer,
                                               IntersectionSerializer)
from geo_platform.apps.common.serializers import ErrorSerializer
from geo_platform.settings import GEOMETRIES_LIMIT
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import DistanceToPointFilter, InBBoxFilter
from rest_framework_gis.pagination import GeoJsonPagination


@extend_schema_view(
    retrieve=extend_schema(
        summary="Inspect an AOI",
        responses={
            200: OpenApiResponse(AOISerializer, description="Success"),
            400: OpenApiResponse(ErrorSerializer, description="Invalid request"),
            404: OpenApiResponse(ErrorSerializer, description="Not found"),
            500: OpenApiResponse(ErrorSerializer, description="Server error"),
        },
    ),
    list=extend_schema(
        summary="List AOIs",
        responses={
            200: OpenApiResponse(AOISerializer, description="Success"),
            400: OpenApiResponse(ErrorSerializer, description="Invalid request"),
            404: OpenApiResponse(ErrorSerializer, description="Not found"),
            500: OpenApiResponse(ErrorSerializer, description="Server error"),
        },
    ),
    analytics=extend_schema(
        summary="Get region analytics",
        parameters=[
            OpenApiParameter(
                "region",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                required=True,
                description="Region",
                examples=[
                    OpenApiExample("Region", value="FR-22"),
                ],
            ),
        ],
        responses={
            200: OpenApiResponse(AnalyticsSerializer, description="Success"),
            400: OpenApiResponse(ErrorSerializer, description="Invalid request"),
            404: OpenApiResponse(ErrorSerializer, description="Not found"),
            500: OpenApiResponse(ErrorSerializer, description="Server error"),
        },
    ),
    intersection=extend_schema(
        summary="Find tiles intersection with given geometry",
        parameters=[
            OpenApiParameter(
                "geometry",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                required=True,
                description="Geometry",
                examples=[
                    OpenApiExample(
                        "geometry",
                        value={
                            "coordinates": [
                                [
                                    [-3.4776011774361564, 50.119580699476074],
                                    [-3.4776011774361564, 43.985106032308806],
                                    [7.56110372177713, 43.985106032308806],
                                    [7.56110372177713, 50.119580699476074],
                                    [-3.4776011774361564, 50.119580699476074],
                                ]
                            ],
                            "type": "Polygon",
                        },
                    ),
                ],
            ),
        ],
        responses={
            200: OpenApiResponse(AOISerializer(many=True), description="Success"),
            400: OpenApiResponse(ErrorSerializer, description="Invalid request"),
            404: OpenApiResponse(ErrorSerializer, description="Not found"),
            500: OpenApiResponse(ErrorSerializer, description="Server error"),
        },
    ),
)
class AOIAPIView(ReadOnlyModelViewSet):
    queryset = AOI.objects.all()
    serializer_class = AOISerializer
    pagination_class = GeoJsonPagination
    bbox_filter_field = AOI.filter_field
    distance_filter_field = AOI.filter_field
    distance_ordering_filter_field = AOI.filter_field
    distance_filter_convert_meters = True
    filter_backends = (
        InBBoxFilter,
        DistanceToPointFilter,
        _DistanceToPointOrderingFilter,
        DjangoFilterBackend,
    )

    filterset_fields = ["crop"]

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        match self.action:
            case "analytics":
                return AnalyticsSerializer
            case "intersection":
                return IntersectionSerializer
            case _:
                return AOISerializer

    @action(methods=["get"], detail=False, permission_classes=(IsAuthenticated,))
    def intersection(self, request):
        query_params = self.request.query_params
        serializer = self.get_serializer_class()(data=query_params)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        geometry = data["geometry"]

        queryset = AOI.objects.filter(geometry__intersects=geometry).all()[
            :GEOMETRIES_LIMIT
        ]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AOISerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AOISerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=False, permission_classes=(IsAuthenticated,))
    def analytics(self, request):
        query_params = self.request.query_params
        self.get_serializer(data=query_params).is_valid(raise_exception=True)
        intersects = AOI.objects.filter(region=query_params["region"]).aggregate(
            total_area=Round(Sum("area_ha", default=0), 3),
            total_yield=Round(Sum("productivity", default=0), 3),
        )
        intersects["average_yield"] = (
            round(intersects["total_yield"] / intersects["total_area"], 3)
            if intersects["total_yield"]
            else 0.0
        )
        return Response(data=intersects)
