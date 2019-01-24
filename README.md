# dengue-backend

* Python 3.6
* pipenv
* Docker 2.0.0.2

## Setup

### Install packages

```python
pipenv install
```

### Postgresql & Postgis

Install Postgresql & Postgis

#### macOS

	brew install postgresql
    brew install postgis
    brew install gdal
    brew install libgeoip

Create user

	createuser -P -e dengue_user
	Enter password for new role: dengue
	Enter it again: dengue
	CREATE ROLE dengue_user PASSWORD ...

Create database

	createdb dengue_db

Grant

	$: psql
	postgres=# GRANT ALL PRIVILEGES ON DATABASE dengue_db TO dengue_user;
    postgres=# \c dengue_db;
    dengue_db=# CREATE EXTENSION postgis;
    CREATE EXTENSION

Initial Database

	python manage.py migrate --settings=dengue.settings.local

### Pillow

#### Ubuntu

    sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

### Redis

Install Redis

    brew install redis

## Setup File

### Insert Hospital

    $: python manage.py shell --settings=dengue.settings.local
    >>> from hospital import load
    >>> load.run('../data/tainan_hospital.tsv')

### Insert Substitute

    $: python manage.py shell --settings=dengue.settings.local
    >>> from taiwan import load
    >>> load.run()

## Start Server

### Redis Server

    redis-server /usr/local/etc/redis.conf

### Local Server

	python manage.py runserver --settings=dengue.settings.local

### Production Server

    sudo uwsgi --ini dengue.ini


## Stop Server

### Production Server

    sudo killall -s INT uwsgi

## Create Superuser

    python manage.py createsuperuser --settings=dengue.settings.local
    Username: admin
    Email address: admin@example.com
    Password: some-secret
    Password: (again): some-secret
    Superuser created successfully.

## Frontend

Install Node.js and npm, we require node v4.x.x or higher and npm 3.x.x or higher.

    cd static/
    npm install
    npm run typings install
    npm tsc


## License
Copyright (c) NCKU The Mosquito Man Project. All rights reserved.

Licensed under the MIT License.
