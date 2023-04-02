from django.contrib.gis import admin

from .models import AOI


@admin.register(AOI)
class AOIAdmin(admin.OSMGeoAdmin):
    readonly_fields = (
        "geometry",
        "pk",
        "created_at",
        "updated_at",
        "user",
    )

    list_display = (
        "pk",
        "region",
        "crop",
        "created_at",
        "updated_at",
        "user",
    )
    list_display_links = ("pk",)
    list_filter = (
        "region",
        "crop",
    )
    search_fields = (
        "pk",
        "user__username",
        "region",
        "crop",
    )
