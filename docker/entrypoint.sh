#!/bin/bash

# Collect all app names
APPS=()
for app in $(find ${WWW_ROOT} -type f -name apps.py); do
    APP_NAME=$(grep -oE "name = '.+'" "$app" | cut -d "'" -f2 | cut -d "'" -f1)
    APPS+=("$APP_NAME")
done

# Flush database, create and apply migrations
python ${WWW_ROOT}/manage.py flush --no-input
python ${WWW_ROOT}/manage.py makemigrations ${APPS[@]} --no-input
python ${WWW_ROOT}/manage.py migrate --no-input

# Create fake data for development. Superuser: ('TestAdmin', 'TestPassword').
python ${WWW_ROOT}/create_fake_data.py

python ${WWW_ROOT}/create_site.py

# Start development server
exec python ${WWW_ROOT}/manage.py runserver 0.0.0.0:8000
