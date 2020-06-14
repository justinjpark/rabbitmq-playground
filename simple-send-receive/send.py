#!/usr/bin/env python

# This program will send messages to the queue


import pika


def send(message):

    # establish a connection with RabbitMQ server
    # connect to RabbitMQ message broker running in Docker container listening on port 5672:5672
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # create the queue to send messages to
    channel.queue_declare(queue='hello')

    # send a message to the queue. . .
    # a message can never be sent directly to the queue, it always needs to go through an exchange
    # the default exchange is special ‒ it allows us to specify exactly to which queue the message should go
    channel.basic_publish(exchange='', routing_key='hello', body=message)

    # print success message and close connection to RabbitMQ
    print(f'Successfully sent message! (message={message})')
    connection.close()


def main():
    send('Hello world!')


if __name__ == '__main__':
    main()
