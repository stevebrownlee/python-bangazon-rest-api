#!/bin/bash

set -a
source .env
set +a

psql -c "DROP DATABASE IF EXISTS $BANGAZON_DB_NAME WITH (FORCE);"
psql -c "CREATE DATABASE $BANGAZON_DB_NAME;"
psql -c "CREATE USER $BANGAZON_DB_NAME WITH PASSWORD '$BANGAZON_DB_PASSWORD';"
psql -c "ALTER ROLE $BANGAZON_DB_NAME SET client_encoding TO 'utf8';"
psql -c "ALTER ROLE $BANGAZON_DB_NAME SET default_transaction_isolation TO 'read committed';"
psql -c "ALTER ROLE $BANGAZON_DB_NAME SET timezone TO 'UTC';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE $BANGAZON_DB_NAME TO $BANGAZON_DB_NAME;"


echo "$BANGAZON_SUPERUSER_PASSWORD"
export DJANGO_SETTINGS_MODULE="bangazon.settings"
GENERATED_PASSWORD=$(python3 ./djangopass.py "$BANGAZON_SUPERUSER_PASSWORD" >&1)

echo '[
    {
        "model": "auth.user",
        "pk": null,
        "fields": {
            "username": "'"$BANGAZON_SUPERUSER_NAME"'",
            "password": "'"$GENERATED_PASSWORD"'",
            "last_login": null,
            "is_superuser": true,
            "first_name": "Admina",
            "last_name": "Straytor",
            "email": "me@me.com",
            "is_staff": true,
            "is_active": true,
            "date_joined": "2023-03-17T17:21:12Z",
            "groups": [ ],
            "user_permissions": []
        }
    }
]' >./bangazonapi/fixtures/superuser.json

python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata customers
python manage.py loaddata product_category
python manage.py loaddata product
python manage.py loaddata productrating
python manage.py loaddata payment
python manage.py loaddata order
python manage.py loaddata order_product
python manage.py loaddata favoritesellers
python manage.py loaddata superuser

rm ./bangazonapi/fixtures/superuser.json
