cd /dengue-backend

python3 dengue/manage.py migrate --settings=dengue.settings.local
python3 dengue/manage.py runserver 0.0.0.0:8000 --settings=dengue.settings.local
