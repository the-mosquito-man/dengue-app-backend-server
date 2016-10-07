# garageDC

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
	pip install -r reuqirements.txt

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

	python manage.py migrate --setting=dengue.settings.local

### Redis

Install Redis

    brew install redis

## Start Server

### Redis Server

    redis-server /usr/local/etc/redis.conf

### Local Server

	python manage.py runserver --setting=dengue.settings.local
