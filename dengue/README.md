# dengue

* Python 3.5
* Django 1.10.1

## Setup

### Create virtualenv

macOS

    pyvenv venv

### Change virtualenv

	source venv/bin/activate

### Install packages

	cd ~/garageDC-webserver
	pip install -r requirements.txt

### Postgresql & Postgis

Install Postgresql & Postgis

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
