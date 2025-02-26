#!/bin/sh

if [ "$POSTGRES_DB" = "date_me" ]
then
    echo "Ждем базу данных..."

    while ! nc -z "db" $POSTGRES_PORT; do
        sleep 0.5
    done

    echo "Postgres запущен"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/zodiac.json
python manage.py loaddata fixtures/compatability.json

exec "$@"