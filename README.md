Список покупок

Django + React + Redux

Деплой:
```
apt install npm uwsgi uwsgi-plugin-python3
vi pyatka/local_settings.py
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
mkdir logs
./manage.py makemigrations api
./manage.py migrate
./manage.py loaddata categories_fixtures.json
./manage.py test --parallel
./manage.py collectstatic --noinput
npm install
npm run build

cp uwsgi.ini /etc/uwsgi/sites-available/pyatka.ini
ln -s /etc/uwsgi/sites-available/pyatka.ini /etc/uwsgi/sites-enabled
systemctl start uwsgi
```
