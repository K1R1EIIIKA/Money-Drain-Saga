from __future__ import absolute_import, unicode_literals

# Это позволяет запускать задачи Celery с помощью Django
from .celery import app as celery_app

__all__ = ('celery_app',)
