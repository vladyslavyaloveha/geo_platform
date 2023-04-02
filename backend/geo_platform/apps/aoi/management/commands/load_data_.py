from typing import Final
import os
import geopandas as gp
import structlog
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from shapely import MultiPolygon, Polygon
from sqlalchemy import create_engine

from geo_platform.apps.aoi.models import AOI

_DATABASE_CONNECTION_STR: Final[str] = 'postgresql://{user}:{password}@{host}:{port}/{database_name}'
_BASE_PATH: Final[str] = '/app/data/'


class Command(BaseCommand):
    help = "Load data to table from given geojson"
    _logger = structlog.get_logger("logger")

    def add_arguments(self, parser) -> None:
        parser.add_argument("--username", help="Username")

    def handle(self, *args, **options) -> None:

        username = options["username"]
        user_model = get_user_model()
        user = user_model.objects.get(username=username)
        path = self._get_geojson_path(_BASE_PATH)
        data = self._read_data(path, user.pk)
        self._upload(data)
        self._logger.info("data uploaded to db", username=username)

    def _get_geojson_path(self, path: str) -> str:
        for filename in os.listdir(path):
            if filename.endswith('.geojsons'):
                abs_path = os.path.join(path, filename)
                self._logger.info("found .geojsons file", abs_path=abs_path)
                return abs_path
        raise ValueError("place .geojsons file for db")

    def _read_data(self, path: str, user_id: str) -> gp.GeoDataFrame:
        self._logger.info("reading data", path=path, user_id=user_id)
        data = gp.read_file(path)
        data.drop(columns=["history", "score"], inplace=True)
        data.rename(columns={"id": "geometry_id"}, inplace=True)
        data["crop"] = data["crop"].fillna("")
        data["region"] = data["region"].fillna("")
        data["user_id"] = user_id
        data["geometry"] = data["geometry"].apply(
            lambda geometry: MultiPolygon([geometry]) if isinstance(geometry, Polygon) else geometry)
        data["geometry"] = data["geometry"].astype("string")
        timestamp = timezone.now()
        data["created_at"] = timestamp
        data["updated_at"] = timestamp
        self._logger.info("data reading finished", size=len(data))
        return data

    @staticmethod
    def _upload(data: gp.GeoDataFrame) -> None:
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']
        port = settings.DATABASES['default']['PORT']
        database_name = settings.DATABASES['default']['NAME']

        database_url = _DATABASE_CONNECTION_STR.format(
            user=user,
            password=password,
            host=host,
            port=port,
            database_name=database_name,
        )
        engine = create_engine(database_url, echo=False)
        data.to_sql(AOI._meta.db_table, con=engine, if_exists="append", index=False)
