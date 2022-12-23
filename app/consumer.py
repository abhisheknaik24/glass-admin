import json

import pika
from django.conf import settings


def on_message_received(ch, method, properties, body):
    body = json.loads(body)
    print("body", body)  # {'task': 'work_order_to_production'}
    ch.basic_ack(delivery_tag=method.delivery_tag)


credentials = pika.PlainCredentials(settings.RABBIT_USER, settings.RABBIT_PASS)

parameters = pika.ConnectionParameters(
    settings.RABBIT_HOST, settings.RABBIT_PORT, "/", credentials
)

connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue="glass_admin")

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue="glass_admin", on_message_callback=on_message_received)
