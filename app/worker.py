from celery import Celery

app = Celery(include=('tasks',))