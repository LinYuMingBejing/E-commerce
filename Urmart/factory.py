import os

from celery import Celery
from django.core.wsgi import get_wsgi_application

from Urmart import settings


def create_app():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Urmart.settings')
    get_wsgi_application()
    app = Celery(__name__)
    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
    return app

