import os

from celery import Celery

# tell Celery where to find the Django project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

# create a new Celery instance and assign to an 'app' variable
app = Celery("api")

# load Celery configuration values from the settings object
# namespace means only variables prefixed with 'CELERY_' will be loaded
app.config_from_object("django.conf:settings", namespace="CELERY")

# tell Celery to look for Celery tasks from applications defined in settings.INSTALLED_APPS
app.autodiscover_tasks()
