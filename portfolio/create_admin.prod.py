import os
import sys
import django
from django.conf import settings
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")
django.setup()

if settings.DEBUG:
    sys.exit("We should NOT be in DEBUG mode!")

ADMIN_FIRST_NAME = os.getenv("DJANGO_ADMIN_FIRST_NAME")
ADMIN_LAST_NAME = os.getenv("DJANGO_ADMIN_LAST_NAME")
ADMIN_USERNAME = os.getenv("DJANGO_ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("DJANGO_ADMIN_PASSWORD")
ADMIN_EMAIL = os.getenv("DJANGO_ADMIN_EMAIL")
if any(
    (s is None or len(s) == 0)
    for s in (
        ADMIN_FIRST_NAME,
        ADMIN_LAST_NAME,
        ADMIN_USERNAME,
        ADMIN_PASSWORD,
        ADMIN_EMAIL,
    )
):
    sys.exit("ADMIN_* not set in .env")

User = get_user_model()

user, created = User.objects.get_or_create(
    username=ADMIN_USERNAME,
    defaults={
        "first_name": ADMIN_FIRST_NAME,
        "last_name": ADMIN_LAST_NAME,
        "email": ADMIN_EMAIL,
        "is_staff": True,
        "is_superuser": True,
    },
)

user.set_password(ADMIN_PASSWORD)
user.is_staff = True
user.is_superuser = True
user.save()
