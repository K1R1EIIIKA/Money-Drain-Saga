from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем default значение для переменной окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# Создаём экземпляр Celery
app = Celery('auth_service')

# Используем конфигурацию RabbitMQ
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автодискавери задач в проектах
app.autodiscover_tasks()

# Настройка брокера сообщений RabbitMQ
app.conf.broker_url = 'amqp://guest:guest@rabbitmq:5672//'
