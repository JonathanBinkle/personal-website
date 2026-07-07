# https://docs.gunicorn.org/en/stable/settings.html

from os import getenv
import socket, multiprocessing

WWW_ROOT = getenv("WWW_ROOT")

chdir = f"{WWW_ROOT}"
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "portfolio.wsgi:application"


### Logging

loglevel = "info"
capture_output = True

# Don't capture access logs (already done by NGINX).
accesslog = None
disable_redirect_access_to_syslog = True

# Send logs via syslog (Docker DNS maps 'syslog' to syslog-ng's IP address)
errorlog = "-"  # cannot be `None`
syslog = True
syslog_prefix = "GUNICORN"
syslog_addr = "udp://syslog:514"
