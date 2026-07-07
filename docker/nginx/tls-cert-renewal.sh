#!/bin/bash

################################################################################
# Tries to renew the Let's Encrypt TLS certificate.
# 
# If something goes wrong, the old certificate can still be used until expiry
# (see https://community.letsencrypt.org/t/19916). Just load the files that are
# backed-up to $TMP into vol/tls/ again.
################################################################################

if [ $(id -u) -ne 0 ]; then
    echo "Must run as root!"
    exit 1
fi

# TODO: you might need to adjust these...
DOMAIN="jonathan.binkle.eu"
DOMAIN_PATH="/etc/letsencrypt/live/$DOMAIN"
CERT_OWNER="jonathan"
PROJECT_ROOT="/home/jonathan/django-portfolio"

cert_validity_days_left() {
    EXPIRY_RAW=$(openssl x509 -enddate -noout -in "$DOMAIN_PATH/fullchain.pem" | cut -d= -f2)
    EXPIRY=$(date -d "$EXPIRY_RAW" +%s)
    NOW=$(date +%s)
    DAYS_LEFT=$(((EXPIRY - NOW) / 86400))
    echo $DAYS_LEFT
}

# Certbot will refuse if we try to renew cert too soon (I believe 30 days).
OLD_DAYS_LEFT=$(cert_validity_days_left)
if [ $OLD_DAYS_LEFT -ge 30 ]; then
    echo "Old cert is still valid for >=30 days. Don't renew yet."
    exit 0
fi

# Backup and teardown containers.
cd "$PROJECT_ROOT"
make create-backup
make enable-maintenance
make teardown-prod

# Create new cert.
certbot renew
if [ $(cert_validity_days_left) -le $OLD_DAYS_LEFT ]; then
    echo "New cert expiry date less or equal to old cert expiry date. Sth went wrong..."
    exit 1
fi

# Backup old certificate files.
# NOTE: also archived under /etc/letsencrypt/, except for the `dhparams4096.pem`
cd $(realpath "$PROJECT_ROOT/docker/nginx/vol/tls/")
TMP=$(mktemp -d)
cp * $TMP/
chown root:root "$TMP"
find "$TMP" -type f -exec chmod 400 {} +
echo "Backed up current certificate files to $TMP"

# Move new certificate files into nginx volume.
rm -rf *
cp -r -L "$DOMAIN_PATH/" .
mv "$DOMAIN/"* .
rmdir "$DOMAIN"
cp $TMP/dhparam4096.pem .
chmod 644 *
chmod 640 privkey.pem
chown $CERT_OWNER:$CERT_OWNER *

# Restart all containers.
cd "$PROJECT_ROOT"
make setup-prod
make enable-maintenance
make restore-backup
make reload-gunicorn
