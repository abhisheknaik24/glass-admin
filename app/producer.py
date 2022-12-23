import json

import pika

connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue="glass_admin")

message = {"task": "work_order_to_production"}

message = json.dumps(message)

channel.basic_publish(exchange="", routing_key="glass_admin", body=message)
