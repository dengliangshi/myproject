#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library


# Third-party libraries
from celery.schedules import crontab

# User define module
from app import mail, celery

# ------------------------------------------------------Global Variables----------------------------------------------------


# -----------------------------------------------------------Main-----------------------------------------------------------
@celery.task(name='tasks.add')
def add(a, b):
    """.
    """
    return a + b

# Periodic Tasks
celery.conf.CELERYBEAT_SCHEDULE = {
    # executes every 30 seconds.
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
    # executes every Friday morning at 8:30 a.m.
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=8, minute=30, day_of_week=5),
        'args': (1, 1),
    },
}