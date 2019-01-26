#!/bin/bash

cd /dengue-backend || exit

python3 dengue/manage.py migrate --settings=dengue.settings.production
python3 dengue/manage.py init_taiwan_data --settings=dengue.settings.production
python3 dengue/manage.py runserver 0.0.0.0:8000 --settings=dengue.settings.production
