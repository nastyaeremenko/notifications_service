import pika
import json


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='default', durable=True)

message = {
    "notification_id": 1,
    "template_path": 'verify_email.html',
    "template_params": {
        "title": "Hello",
        "body": "Hello World",
        "first_name": "Dima",
        "last_name": "Vokhmin"
    },
    "subject": 'some subject',
    "email": 'boxdima1@gmail.com'
}
channel.basic_publish(
    exchange='',
    routing_key='default',
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))
print(" [x] Sent %r" % message)
connection.close()
