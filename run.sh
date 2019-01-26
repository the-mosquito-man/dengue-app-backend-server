#!/bin/bash

cd /dengue-backend || exit

echo "Migrating database"
python3 dengue/manage.py migrate --settings=dengue.settings.production

if [ "$INIT_DB" = true ]
then
    echo "Initialize Hospital Data"
    python3 dengue/manage.py init_hospital_data --settings=dengue.settings.production

    echo "Initialize Taiwan Data"
    python3 dengue/manage.py init_taiwan_data --settings=dengue.settings.production
fi

echo "Run Server"
python3 dengue/manage.py runserver 0.0.0.0:8000 --settings=dengue.settings.production
