# Dengue App - Backend Server

## Table of content
* [Getting Started](#sec-1)
* [Run dengue-backend OUTSIDE Docker Container](#sec-2)
* [Run dengue-backend INSIDE Docker Container](#sec-3)
* [License](sec-4)

<a name='sec-1'></a>
## Getting Started

### Prerequistes

* [Python3.6](https://www.python.org/downloads/)
* [pipenv](https://pipenv.readthedocs.io/en/latest/)
* [Node.js](https://nodejs.org/en/)
* [npm](https://www.npmjs.com)
* [npx](https://www.npmjs.com/package/npx)
* [Docker](https://docs.docker.com/engine/installation/)
* [postgresql](https://www.postgresql.org/download/)
* [postgis](https://postgis.net/install/)
* [Pillow](https://github.com/python-pillow/Pillow)

#### Install Postgis on macOS

```sh
brew install PostgreSQL
brew install postgis
brew install gdal
brew install libgeoip
```

#### Install Redis on macOS

```sh
brew install redis
```

#### Install Pillow Dependency on Ubuntu

```sh
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
```


<a name='sec-2'></a>
## Run dengue-backend OUTSIDE Docker Container

### Setup Backend

* Install Backend Packages

```sh
pipenv install
```

* Setup environment variables

```sh
export DENGUE_SECRET_KEY="some hard to guess value"
export DENGUE_DB_NAME="database name for postgis"
export DENGUE_DB_USER="user name for postgis"
export DENGUE_DB_PASSWORD="user password for postgis"
export DENGUE_DB_HOST="host for postgis"
export DENGUE_DB_PORT="port for postgis"
export DENGUE_CACHE_LOCATION="redis uri"
export AWS_ACCESS_KEY="AWS access key"
export AWS_SECRET_KEY="AWS secret key"
export GOOGLE_MAP_API_KEY="Google Map API key"
```

### Setup Postgis

* Create user

```sh
$ createuser -P -e dengue_user

Enter password for new role: dengue
Enter it again: dengue
CREATE ROLE dengue_user PASSWORD ...
```

* Create database

```sh
createdb dengue_db
```

* Start Postgres server

```sh
pg_ctl -D /usr/local/var/postgres start
```

* Create postgis extension

```sh
$ psql

postgres=# GRANT ALL PRIVILEGES ON DATABASE dengue_db TO dengue_user;
postgres=# \c dengue_db;
dengue_db=# CREATE EXTENSION postgis;
CREATE EXTENSION
```

* Initial Database
    * Different <ENV> can be configed in `dengue/dengue/settings`

```sh
pipenv run python dengue/manage.py migrate --settings=dengue.settings.<ENV>
```

* Create Superuser
    * Different <ENV> can be configed in `dengue/dengue/settings`

```sh
$ pipenv run python dengue/manage.py createsuperuser --settings=dengue.settings.<ENV>

Username: admin
Email address: admin@example.com
Password: some-secret
Password: (again): some-secret
Superuser created successfully.
```

* Initialize Data
    * Different <ENV> can be configed in `dengue/dengue/settings`

```sh
# Insert Substitute
pipenv run python dengue/manage.py init_taiwan_data --settings=dengue.settings.<ENV>

# Insert Hospitial
pipenv run python dengue/manage.py init_hospital_data --settings=dengue.settings.<ENV>
```


### Setup Redis

* Start

```sh
redis-server
```

### Setup Frontend

```sh
cd dengue/static/
npm install
npm run typings install
npx tsc
```

### Start Backend Server

* Start a local server
  * Different <ENV> can be configed in `dengue/dengue/settings`

```sh
pipenv run python dengue/manage.py runserver --settings=dengue.settings.<ENV>
```

* Start production server

```sh
cd dengue/
sudo uwsgi --ini dengue.ini
```

* Stop production server

```sh
sudo killall -s INT uwsgi
```

<a name="sec-3"></a>

## Run dengue-backend INSIDE Docker Container

* Setup environement variables by creating `env.cfg` at the root directory (Use `env-template.cfg` as the template for `env.cfg`)
  * Note that the following key pairs should have the same value
    * `POSTGRES_DBNAME`, `DENGUE_DB_NAME`
    * `DENGUE_DB_USER`, `POSTGRES_USER`
    * `DENGUE_DB_PASSWORD`, `POSTGRES_PASS`
  * `INIT_DB` should be true and `GOOGLE_MAP_API_KEY` should be proper API key only when the database is first created and used to initial data
  * The hostname and other nginx configuration can be configured in. `docker/nginx`.

```sh
docker-compose build
docker-compose up -d
```

### Migrate Database Manually
It's possible that the "web" container runs before "postgis" contain is ready and thus cannot migrate database in time.  
If this happens, you will get a 502 response when you enter http://127.0.0.1.  
In such case, you should manually migrate the database.

Use `docker ps` command to find the container ID of "dengue-backend_web" and execute the following command to migrate the database.

```sh
docker exec -it <CONTAINER ID>  python3 dengue/manage.py migrate --settings=dengue.settings.production
```

### Create Super User

```sh
docker exec -it <CONTAINER ID>  python3 dengue/manage.py createsuperuser --settings=dengue.settings.production
```

### Clean Up Docker Image and Volumes (Use with Cautious)
Note that this command will clean up all the data.

```sh
docker-compose down -v --rmi local
```

<a name="sec-4"></a>

## License

Copyright (c) NCKU The Mosquito Man Project. All rights reserved.

Licensed under the MIT License.
