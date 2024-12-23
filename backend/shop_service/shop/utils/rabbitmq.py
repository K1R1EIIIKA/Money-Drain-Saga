import pika
import json

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672

def send_spend_money_request(user_id, item_id, money, token):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
    channel = connection.channel()

    # Убедимся, что очередь существует
    channel.queue_declare(queue='spend_money', durable=True)

    message = {
        'user_id': user_id,
        'item_id': item_id,
        'money': money,
        'token': token,
    }

    # Отправка сообщения в очередь
    channel.basic_publish(
        exchange='',
        routing_key='spend_money',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Сообщение будет сохраняться на диске
        )
    )

    print("Сообщение отправлено в очередь для обработки")
    connection.close()
