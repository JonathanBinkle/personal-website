import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")
django.setup()

from django.conf import settings
from django.contrib.sites.models import Site

site = Site.objects.get(pk=settings.SITE_ID)
site.domain = settings.SITE_DOMAIN
site.name = settings.SITE_NAME
site.save()
