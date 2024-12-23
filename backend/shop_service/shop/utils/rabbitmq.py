import pika
import json

def send_message_to_queue(queue_name, message):
    # Настроим подключение и канал RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    # Создаем очередь с параметром durable=True, если она не существует
    channel.queue_declare(queue=queue_name, durable=True)

    # Преобразуем сообщение в формат JSON и отправляем его в очередь
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # сообщение будет сохраняться на диске (durable)
        )
    )

    print(f"Сообщение отправлено в очередь {queue_name}")
    connection.close()
