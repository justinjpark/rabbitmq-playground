#!/usr/bin/env python

# This program will schedule tasks to our work queue (task queue)

# run two instances of worker.py, then in a third console publish the follow new tasks:
# ./new_task.py First message.
# ./new_task.py Second message..
# ./new_task.py Third message...
# ./new_task.py Fourth message....
# ./new_task.py Fifth message.....

# By default, RabbitMQ will send each message to the next consumer, in sequence.
# On average every consumer will get the same number of messages.
# This way of distributing messages is called round-robin.


import pika
import sys


def new_task():
    # establish a connection with RabbitMQ server
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # ensure that the queue exists, declare (or create) the queue
    # ensure that the queue will survive a RabbitMQ node restart by declaring it as durable
    channel.queue_declare(queue='task_queue', durable=True)

    # read in command line argument as message and send to queue
    message = ' '.join(sys.argv[1:]) or 'Hello world!'

    # ensure messages are persistent by setting the delivery_mode property to 2
    properties = pika.BasicProperties(delivery_mode=2)

    # send a message to the queue and close connection
    channel.basic_publish(exchange='', routing_key='task_queue', body=message, properties=properties)
    print(f'Successfully sent message! (message={message})')
    connection.close()


def main():
    new_task()


if __name__ == '__main__':
    main()
