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


#### Geojson schema example
`{ "type": "Feature", "properties": { "id": 0, "crop": "wheat", "productivity": 0.75, "area_ha": "0.3", "history": "null", "region": "FR-29", "score": null }, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ -3.9372747, 48.3130477 ], [ -3.9373466, 48.3132057 ], [ -3.937404, 48.31322 ], [ -3.9374614, 48.3131626 ], [ -3.9375189, 48.3131051 ], [ -3.9375764, 48.3130477 ], [ -3.9376338, 48.3129902 ], [ -3.9377056, 48.3129472 ], [ -3.9377918, 48.3129184 ], [ -3.9378349, 48.3128753 ], [ -3.9378062, 48.3128179 ], [ -3.9377487, 48.3127604 ], [ -3.9376912, 48.3126743 ], [ -3.9376194, 48.3125306 ], [ -3.9375189, 48.312387 ], [ -3.9374184, 48.3123008 ], [ -3.9373466, 48.3122721 ], [ -3.9372747, 48.3123008 ], [ -3.9371598, 48.3123439 ], [ -3.9370306, 48.3123727 ], [ -3.9369731, 48.3124157 ], [ -3.9370019, 48.3125019 ], [ -3.9370737, 48.3126455 ], [ -3.9371742, 48.3128323 ], [ -3.9372747, 48.3130477 ] ] ] ] } }`
