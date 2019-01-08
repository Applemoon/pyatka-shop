Список покупок

Django + React + Redux

Деплой:
vi pyatka/local_settings.py
apt install npm uwsgi uwsgi-plugin-python3
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
./manage.py makemigrations api
./manage.py migrate
./manage.py loaddata categories_fixtures.json
./manage.py collectstatic --noinput
npm install
npm run build
mkdir logs
./run_uwsgi.sh

