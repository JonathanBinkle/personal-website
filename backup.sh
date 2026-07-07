#!/bin/bash

################################################################################
# Send backups to storage box.
# A host `backupbox` must be configured in /root/.ssh/config.
# Create cronjob (`sudo crontab -e`):
# 0 1 * * * /home/jonathan/django-portfolio/backup.sh | /usr/bin/logger -t CRON
#
# TODO: prior encryption of backups (e.g. using `borg`) would be nice...
################################################################################

[[ $EUID -ne 0 ]] && { echo "Script must run as root"; exit 1; }

cd "$(dirname "$0")"

make create-backup

for file in backup*.tar.gz; do
    [ -e "$file" ] || continue
    scp "$file" backupbox:/home/
done
