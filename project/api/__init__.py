from .celery import app as celery_app


# so that the Celery app is automatically imported when Django starts
__all__ = ("celery_app",)
