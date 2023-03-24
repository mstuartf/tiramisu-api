"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
from datetime import timedelta

from kombu.utils.url import safequote
from django.utils.log import DEFAULT_LOGGING

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Useful to know if we are running tests
TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",") + ["app"]
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"django.server": DEFAULT_LOGGING["formatters"]["django.server"]},
    "handlers": {
        # In ECS, logs streamed to STDOUT/STDERR (i.e. 'console' handler) will be sent to Cloudwatch.
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
        "django.server": DEFAULT_LOGGING["handlers"]["django.server"]
        # TODO: when should alert emails be sent to admins?
        # 'mail_admins': DEFAULT_LOGGING['handlers']['mail_admins']
    },
    "loggers": {
        # everything > WARNING should be logged (inc 3rd party)
        "": {
            "level": "WARNING",
            "handlers": ["console"],
        },
        # but log everything > configurable LOG_LEVEL from our own code (this is why all apps are located in apps/)
        "apps": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            # required to avoid double logging with root logger above
            "propagate": False,
        },
        "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
    },
}


# Application definition

INSTALLED_APPS = [
    "channels",
    "corsheaders",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.accounts",
    "apps.companies",
    "apps.prompts",
    "apps.prospects",
    "apps.messages",
    "apps.templates",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    'ROTATE_REFRESH_TOKENS': True
}

AUTH_USER_MODEL = "accounts.CustomUser"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "django.contrib.auth.backends.RemoteUserBackend",
]

ROOT_URLCONF = "api.urls"

LOGIN_REDIRECT_URL = "/accounts/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOSTNAME"),
        "PORT": "5432",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# path to the dir where collectstatic will place static files
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# URL that serves the files collected
STATIC_URL = "/static/"

# tell collect static to look in the api app's static folder
# as well as the default locations (static dirs of INSTALLED_APPS)
STATICFILES_DIRS = [os.path.join(BASE_DIR, "api/static")]

# CELERY

# Note: these are set to fake values locally in `docker-compose.yml`.
aws_access_key_id = os.environ.get("CELERY_ACCESS_KEY_ID", "")
aws_secret_access_key = os.environ.get("CELERY_SECRET_ACCESS_KEY", "")

# this environment variable only needs to be set locally otherwise leave as empty string
sqs_host = os.environ.get("CELERY_HOST_AND_PORT", "")

CELERY_BROKER_URL = (
    "sqs://{aws_access_key_id}:{aws_secret_access_key}@{host_and_port}".format(
        aws_access_key_id=safequote(aws_access_key_id),
        aws_secret_access_key=safequote(aws_secret_access_key),
        host_and_port=sqs_host,
    )
)

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

# https://stackoverflow.com/a/55362566/15793866
CELERY_TASK_DEFAULT_QUEUE = os.environ.get("CELERY_QUEUE_NAME")

# Disable the results backend (need to enable if we want to check on pending tasks)
CELERY_RESULT_BACKEND = None

CELERY_BROKER_TRANSPORT_OPTIONS = {
    "region": "eu-west-2",
}
