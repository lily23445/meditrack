import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_project.settings")

app = Celery("demo_project")

# Load task modules from all registered Django apps.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
