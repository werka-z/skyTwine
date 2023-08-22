from django.conf import settings
from celery import Celery
import os
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skyTwine.settings')

app = Celery('skyTwine', broker='memory://')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'run-daily-updates': {
        'task': 'weather.tasks.daily_updates',
        'schedule': 3600,  # Runs every hour - 3600 s
    }
}
