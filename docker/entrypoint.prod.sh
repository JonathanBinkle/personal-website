#!/bin/bash

# Collect static files into settings.py > STATIC_ROOT
python ${WWW_ROOT}/manage.py collectstatic --noinput --clear

# Flush and apply migrations
python ${WWW_ROOT}/manage.py flush --no-input
python ${WWW_ROOT}/manage.py migrate --no-input

# Create admin account
python ${WWW_ROOT}/create_admin.prod.py

# Create site for sitemap to show correct domain
python ${WWW_ROOT}/create_site.py

# Start gunicorn
exec python -m gunicorn -c ${APP_ROOT}/gunicorn.conf.py --preload
