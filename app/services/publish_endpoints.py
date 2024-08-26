import pika
import json


def publish_endpoints():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='endpoints_queue')

    # Собираем информацию о эндпоинтах
    endpoints = [
        {'path': '/products/get/', 'method': 'GET'},
        # Добавьте другие эндпоинты здесь
    ]

    # Отправляем информацию в RabbitMQ
    channel.basic_publish(exchange='',
                          routing_key='endpoints_queue',
                          body=json.dumps(endpoints))

    print("Endpoints sent")
    connection.close()


# Запустите эту функцию, когда нужно отправить информацию


