#!/usr/bin/env python

# This program will receive messages from the queue and print them on the screen


import pika


def receive():

    # establish a connection with RabbitMQ server
    # connect to RabbitMQ message broker running in Docker container listening on port 5672:5672
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # ensure that the queue exists, declare (or create) the queue
    # it is a good practice to repeat declaring the queue in both programs
    channel.queue_declare(queue='hello')

    # whenever a message is recieved, this callback function is called by the Pika library
    # in our case, it will print out the body of the message
    def callback(ch, method, properties, body):
        message = body.decode("utf-8") 
        print(f'Successfully received message! (body={message})')

    # tell RabbitMQ that our callback function should receive messages from the queue
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    # enter a never-ending loop that waits for data (messages) and runs callbacks whenever necessary
    print('Waiting for messages. . . To exit press CTRL+C')
    channel.start_consuming()


def main():
    receive()


if __name__ == '__main__':
    main()
