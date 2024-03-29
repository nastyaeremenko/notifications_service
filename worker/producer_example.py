import json

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Замените 'default' на название очереди для определенного сценария. Они лежат в файле queue.txt
queue_name = 'email_confirm'

channel.queue_declare(queue=queue_name,
                      durable=True)

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
    "email": 'boxdima1@gmail.com',
    "is_last": True
}
channel.basic_publish(
    exchange='',
    routing_key=queue_name,
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))
print(" [x] Sent %r" % message)
connection.close()
