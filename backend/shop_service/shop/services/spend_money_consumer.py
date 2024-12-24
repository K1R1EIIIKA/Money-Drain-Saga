import pika
import json
import requests
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'shop_service.settings')
django.setup()
from shop.models import UserItem

RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672
AUTH_SERVICE_URL = 'http://localhost:8000/user'
SPEND_MONEY_URL = 'http://localhost:8000/money/spend'


def get_user_data(user_id, token):
    headers = {"jwt": token}
    response = requests.get(AUTH_SERVICE_URL, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка получения данных пользователя: {response.status_code} {response.text}")
        return None

    return response.json()


def spend_money(user_id, token, amount):
    headers = {"jwt": token}
    print(amount)
    data = {"money": amount}
    response = requests.post(SPEND_MONEY_URL, headers=headers, json=data)

    if response.status_code != 200:
        print(123)
        print(f"Ошибка списания средств: {response.status_code} {response.text}")
        return False

    return True


def spend_money_callback(ch, method, properties, body):
    try:
        print("Сообщение получено.")
        data = json.loads(body)

        user_id = data.get("user_id")
        item_id = data.get("item_id")
        token = data.get("token")

        if not user_id or not item_id or not token:
            print("Некорректные данные задачи")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        user_data = get_user_data(user_id, token)
        if not user_data:
            print(f"Пользователь с ID {user_id} не найден.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        user_money = user_data.get("money", 0)
        item_price = 100

        if user_money < item_price:
            print(f"Недостаточно средств у пользователя {user_id}.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        if not spend_money(user_id, token, item_price):
            print(f"Не удалось списать средства у пользователя {user_id}.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        user_item = UserItem.objects.create(user_id=user_id, item_id=item_id)
        user_item.save()

        print(f"Покупка выполнена: пользователь {user_id} купил товар {item_id}.")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Ошибка при обработке сообщения: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
    channel = connection.channel()

    channel.queue_declare(queue='spend_money', durable=True)
    channel.basic_consume(queue='spend_money', on_message_callback=spend_money_callback)

    print("Ожидание сообщений...")
    channel.start_consuming()


if __name__ == '__main__':
    start_consumer()
