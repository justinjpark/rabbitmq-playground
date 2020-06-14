#!/usr/bin/env python

# This program will receive messages from the queue and print them on the screen


import pika
import time


def worker():

    # establish a connection with RabbitMQ server
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # ensure that the queue exists, declare (or create) the queue
    # ensure that the queue will survive a RabbitMQ node restart by declaring it as durable
    channel.queue_declare(queue='task_queue', durable=True)

    # whenever a message is recieved, this callback function is called by the Pika library
    def callback(ch, method, properties, body):
        message = body.decode("utf-8") 
        print(f'Successfully received message! (body={message})')
        time.sleep(message.count('.')) # pretend work is being done for task
        print (f'. . .completed task. (body={message})')
        
        # Using this code, we can ensure that even if you kill a worker using CTRL+C while it is processing a message, 
        # nothing will be lost. Soon after the worker dies all unacknowledged messages will be redelivered.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # tell RabbitMQ to not dispatch a new message to a worker until it has processed and acknowledged the previous one
    # (to not give more than 1 message to a worker at a time)
    channel.basic_qos(prefetch_count=1)

    # tell RabbitMQ that our callback function should receive messages from the queue
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    # enter a never-ending loop that waits for data (messages) and runs callbacks whenever necessary
    print('Waiting for messages. . . To exit press CTRL+C')
    channel.start_consuming()


def main():
    worker()  


if __name__ == '__main__':
    main()
