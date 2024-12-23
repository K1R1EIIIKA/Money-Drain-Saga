import os

import django
import pika


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'transactions_service.settings')
django.setup()
from transactions.models import Transaction

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672

def add_transaction(ch, method, properties, body):
    print(f"Received transaction: {body}")
    body = dict(eval(body))
    user_id = body['user_id']
    amount = body['amount']
    currency = body['currency']
    status = body['status']

    # Сохраняем транзакцию в базу данных
    transaction = Transaction.objects.create(user_id=user_id, amount=amount, currency=currency, status=status)
    print(f"Transaction saved: {transaction}")
    transaction.save()

    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
    channel = connection.channel()

    # Убедимся, что очередь существует
    channel.queue_declare(queue='add_transaction', durable=True)

    # Подключаем callback-функцию
    channel.basic_consume(queue='add_transaction', on_message_callback=add_transaction)

    print("Ожидание сообщений...")
    channel.start_consuming()


if __name__ == '__main__':
    start_consumer()
