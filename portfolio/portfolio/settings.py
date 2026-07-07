import os
import socket
from pathlib import Path
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# Nginx tells Django via X_FORWARDED_PROTO whether it was HTTP/S request
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# HSTS is enabled by NGINX, so, no need to do this here again.

# Django's CSRF protection needs the Referer header for HTTPS, thus, don't set
# to 'no-referrer'.
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.getenv("DEBUG", "0")) == 1

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(" ")
CSRF_TRUSTED_ORIGINS = [
    "https://" + origin for origin in os.getenv("CSRF_TRUSTED_ORIGINS").split(" ")
]

# Secure cookies: HttpOnly, Secure, SameSite=Lax
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_HTTPONLY = True

# Sitemap
SITE_ID = 1
SITE_DOMAIN = os.getenv("DJANGO_SITE_DOMAIN")
if SITE_DOMAIN is None or len(SITE_DOMAIN) == 0:
    sys.exit("DJANGO_SITE_DOMAIN should be set in .env")
SITE_NAME = SITE_DOMAIN

# Application definition
CUSTOM_APPS = ["blog", "core"]
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Sitemap
    "django.contrib.sites",
    "django.contrib.sitemaps",
]
INSTALLED_APPS += CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # custom
    "core.middleware.CSPMiddleware",
]

ROOT_URLCONF = "portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # custom
                "core.context_processors.csp_nonce",
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": os.getenv("MYSQL_HOST"),
        "PORT": os.getenv("MYSQL_PORT"),
        "OPTIONS": {
            # https://docs.djangoproject.com/en/4.2/ref/databases/#creating-your-tables
            "init_command": "SET default_storage_engine=INNODB;"
        },
    }
}

if DEBUG:
    # No test database in production
    DATABASES["default"].update({"TEST": {"NAME": os.getenv("MYSQL_TEST_DATABASE")}})


# -------
# Logging: If DEBUG log to console else log to a centralized syslog-ng container
# -------
# https://riptutorial.com/django/example/4028/logging-to-syslog-service
# https://docs.djangoproject.com/en/4.2/topics/logging/
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            # If you want to include time: [%(asctime)s] (but syslog-ng does
            # that anyway). Also do: 'datefmt' : "%d/%b/%Y %H:%M:%S"
            "format": "DJANGO [%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console" if DEBUG else "syslog"],
            "level": "INFO",
            "disabled": False,
            "propagate": True,
        }
    },
}

if not DEBUG:
    LOGGING["handlers"].update(
        {
            "syslog": {
                "class": "logging.handlers.SysLogHandler",
                "address": (socket.gethostbyname("syslog"), 514),
                "formatter": "standard",
            }
        }
    )

LOGGING["loggers"].update(
    {
        app: {"handlers": ["console" if DEBUG else "syslog"], "propagate": True}
        for app in INSTALLED_APPS
    }
)

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

APP_ROOT = os.getenv("APP_ROOT")
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "blog/static",
]
STATIC_ROOT = f"{APP_ROOT}/staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = f"{APP_ROOT}/mediafiles"

FILE_UPLOAD_PERMISSIONS = 0o600

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
