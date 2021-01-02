from celery import Celery
import django
import os

from Urmart import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Urmart.settings')
django.setup()
app = Celery(__name__, broker='redis://127.0.0.1:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

