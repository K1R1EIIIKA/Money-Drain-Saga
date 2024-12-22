from celery import shared_task
import pika
import json

@shared_task
def send_registration_notification(user_id, username):
    # Создание сообщения для отправки в RabbitMQ
    message = {
        'user_id': user_id,
        'username': username
    }

    # Подключение к RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', pika.PlainCredentials('guest', 'guest')))
    channel = connection.channel()

    # Объявляем очередь
    channel.queue_declare(queue='user_notifications')

    # Отправляем сообщение в очередь
    channel.basic_publish(exchange='',
                          routing_key='user_notifications',
                          body=json.dumps(message))

    print(f"Sent message to queue: {message}")

    # Закрытие соединения
    connection.close()
