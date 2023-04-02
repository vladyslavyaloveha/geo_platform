# Geo Platform
___
### Geo Platform provides simple API that retrieves geometries from the preloaded database by given parameters.

## Configuration
___
Add `.env` file with environment variables to `geo_platform folder`:
```
# Entrypoint
DJANGO_COLLECTSTATIC=1
DJANGO_COMPILEMESSAGES=1
DJANGO_MIGRATE=1

# Path to directory with .geojson file
DATA_PATH=/geo_platform/data

# Database
DB_PORT=5432
DB_HOST=db
DB_NAME=db
DB_USER=user
DB_PASSWORD=database

# Auth
SECRET_KEY=04938539048hvkldvnsd30495484ry4fhkwejgf

# Super user
SUPERUSER_USERNAME=admin
SUPERUSER_EMAIL=admin
SUPERUSER_PASSWORD=admin
```
## Run
1. Please, download and place valid `.geojsons` file and set `DATA_PATH` env variable. <br>
2. For development purpose: <br>
`docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build`
3. Production run: <br>
`docker-compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.prod.yml up --build`

## Documentation

Visit `http://localhost:80/api/docs` for full documentation and `http://localhost:80/api/admin` for Admin website.

###  Main features
1. User registration and JWT Auth. The superuser was created and exists in system.
2. Endpoints implement next features:
* Get the set of fields that are "nearby" given point within a given distance. Point and distance are sent by the user (in meters).
* Get the set of fields that are inside the bound box.
* Get the set of fields that intersect with the requested geometry.
* Get the area, yield, and average yield per hectare in a region that was sent by the user.
