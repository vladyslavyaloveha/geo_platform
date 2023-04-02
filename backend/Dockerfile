FROM python:3.10 as build

WORKDIR /dist

COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade --no-cache-dir poetry==1.4.2 \
  && poetry export -f requirements.txt --output requirements.txt  \
  --without-hashes


FROM python:3.10 AS final

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY --from=build /dist/requirements.txt requirements.txt
RUN apt-get update \
  && apt-get install -y binutils libproj-dev gdal-bin \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --upgrade --no-cache-dir gunicorn==20.1.0 \
  && pip install --upgrade --no-cache-dir -r requirements.txt \
  && rm -f requirements.txt \
  && mkdir -p /app/logs
COPY scripts/docker-entrypoint.sh manage.py ./
COPY geo_platform geo_platform

EXPOSE 80

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["-b", "0.0.0.0:80", "geo_platform.wsgi"]
