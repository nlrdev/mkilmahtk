from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config.celery", broker="amqp://devmin:devmin@prod_mq:5672/dochost")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
