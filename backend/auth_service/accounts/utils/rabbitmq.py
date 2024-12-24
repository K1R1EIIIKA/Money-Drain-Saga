import pika
import json

RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672

def send_transaction_request(user_id, amount, currency, status):
    message = {
        'user_id': user_id,
        'amount': amount,
        'currency': currency,
        'status': status
    }

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT))
    channel = connection.channel()

    channel.queue_declare(queue='add_transaction', durable=True)

    channel.basic_publish(exchange='',
                          routing_key='add_transaction',
                          body=json.dumps(message),
                            properties=pika.BasicProperties(
                                delivery_mode=2,
                            ))

    print(f"Sent transaction request: {message}")

    connection.close()