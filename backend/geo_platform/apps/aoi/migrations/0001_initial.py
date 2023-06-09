# Generated by Django 4.2 on 2023-04-17 13:16

from django.conf import settings
from django.contrib.gis.db.models import fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AOI",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("geometry_id", models.PositiveIntegerField()),
                ("crop", models.TextField(blank=True, max_length=120)),
                ("productivity", models.FloatField(null=True)),
                ("region", models.TextField(blank=True, max_length=100)),
                ("area_ha", models.FloatField(null=True)),
                (
                    "geometry", fields.MultiPolygonField(srid=4326, spatial_index=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
