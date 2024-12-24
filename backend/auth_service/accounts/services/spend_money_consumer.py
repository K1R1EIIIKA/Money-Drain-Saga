import os

import django
import requests

from accounts.utils.rabbitmq import send_transaction_request

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'auth_service.settings')
django.setup()

import pika
import json

from django.contrib.auth import get_user_model

User = get_user_model()
RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672

def spend_money_from_message(ch, method, properties, body):
    try:
        data = json.loads(body)
        user_id = data.get('user_id')
        item_id = data.get('item_id')
        token = data.get('token')
        token = token.split(" ")[1]
        money = data.get('money')

        if not all([user_id, item_id, token]):
            print(f"Некорректные данные: {data}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        URL = 'http://authservice:8000/money/spend'

        result = requests.post(URL, data={"money": int(money)}, headers={"jwt": token})
        if result:
            print(f"Средства списаны: {result}")
        else:
            print(f"Ошибка при списании средств: {result.text}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

        status = 'completed' if result else 'failed'
        send_transaction_request(user_id, item_id, money, status)

    except Exception as e:
        print(f"Ошибка при обработке сообщения: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
    channel = connection.channel()

    channel.queue_declare(queue='spend_money', durable=True)

    channel.basic_consume(queue='spend_money', on_message_callback=spend_money_from_message)

    print("Ожидание сообщений...")
    channel.start_consuming()


if __name__ == '__main__':
    start_consumer()
