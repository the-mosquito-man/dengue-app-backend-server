# dengue-backend

## Getting Started
### Prerequistes
* [Python3.6](https://www.python.org/downloads/)
* [pipenv](https://pipenv.readthedocs.io/en/latest/)
* [Node.js](https://nodejs.org/en/)
* [npm](https://www.npmjs.com)
* [Docker](https://docs.docker.com/engine/installation/)
* [postgresql](https://www.postgresql.org/download/)
* [postgis](https://postgis.net/install/)
* [Pillow](https://github.com/python-pillow/Pillow)

### Install Dependency for Pillow

* For Ubuntu User

```sh
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
```

### Install Backend Packages

```python
pipenv install
```


## Run dengue-backend OUTSIDE Docker Container

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
$ createdb dengue_db
```

* Grant

```sh
$ psql

postgres=# GRANT ALL PRIVILEGES ON DATABASE dengue_db TO dengue_user;
postgres=# \c dengue_db;
dengue_db=# CREATE EXTENSION postgis;
CREATE EXTENSION
```

* Initial Database

```sh
$ pipenv python manage.py migrate --settings=dengue.settings.<ENV>
```

* Create Superuser

```sh
$ python manage.py createsuperuser --settings=dengue.settings.<ENV>

Username: admin
Email address: admin@example.com
Password: some-secret
Password: (again): some-secret
Superuser created successfully.
```

* Intialize Data

```sh
$ python dengue/manage.py shell --settings=dengue.settings.<ENV>

# Insert Hospitial
>>> from hospital import load
>>> load.run('data/tainan_hospital.tsv')

# Insert substitue
>>> from taiwan import load
>>> load.run()
```

* Start

```sh
pg_ctl -D /usr/local/var/postgres start
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


* Setup environment variables

```sh
$ export DENGUE_SECRET_KEY="some hard to guess value"
$ export DENGUE_DB_NAME="database name for postgis"
$ export DENGUE_DB_USER="user name for postgis"
$ export DENGUE_DB_PASSWORD="user password for postgis"
$ export DENGUE_DB_HOST="host for postgis"
$ export DENGUE_DB_PORT="port for postgis"
$ export DENGUE_CACHE_LOCATION="redis uri"
$ export AWS_ACCESS_KEY="AWS access key"
$ export AWS_SECRET_KEY="AWS secret key"
```

* Start local server

```sh
python manage.py runserver --settings=dengue.settings.<ENV>
```

* Start production server

```
sudo uwsgi --ini dengue.ini
```

* Stop production server

```sh
sudo killall -s INT uwsgi
```

## Run dengue-backend INSIDE Docker Container

* Create `env.cfg` at the root (`env-template.cfg` is the template for `env.cfg`)
	* Note that the following key pairs should have the same value
		* POSTGRES_DBNAME, DENGUE_DB_NAME
		* DENGUE_DB_USER, POSTGRES_USER
		* DENGUE_DB_PASSWORD, POSTGRES_PASS

```sh
docker-compose build
docker-compose up
```		  


## License
Copyright (c) NCKU The Mosquito Man Project. All rights reserved.

Licensed under the MIT License.
