#!/usr/bin/env python

# This is the producer program (a producer is a user application that sends messages), which emits log messages
# This program uses a fanout exchange (broadcasts all the messages it receives to all the queues it knows)

# Run multiple instances of receive_logs.py, then use a seperate console to publish logs
# The fanout exchange should relay messages to all instances of receive_logs.py using their server-assigned queue names


import pika
import sys


def fanout_log():

    # establish a connection with RabbitMQ server
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declare the fanout exchange
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # read in command line argument as message, send to queue, and close connection
    # remember, fanout exchanges broadcasts messages, so the routing_key is ignored
    message = ' '.join(sys.argv[1:]) or 'default: Hello world!'
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print(f'Successfully sent message! (message={message})')
    connection.close()


def main():
    fanout_log()


if __name__ == '__main__':
    main()
