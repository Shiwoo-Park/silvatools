import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silvatools.settings.local")

app = Celery("silvatools")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# celery configuration
# https://docs.celeryproject.org/en/latest/userguide/configuration.html

# Priority queue setup
app.conf.task_queue_max_priority = 10
app.conf.task_default_priority = 5

# Load task modules from all registered Django app configs.
# default (search "tasks" module in each apps in INSTALLED_APPS)
app.autodiscover_tasks()

# Setup periodic tasks by celery-beat
# https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules
app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    "add-every-monday-morning": {
        "task": "tasks.add",
        "schedule": crontab(hour=7, minute=30, day_of_week=1),
        "args": (16, 16),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
