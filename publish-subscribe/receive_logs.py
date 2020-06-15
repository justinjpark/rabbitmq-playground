#!/usr/bin/env python

# This is the consumer program (a consumer is a user application that receives message)


import pika


def receive_logs():

    # establish a connection with RabbitMQ server
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declare the fanout exchange
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # declare (create) a queue with a random name (RabbitMQ server supplies the random queue name)
    # exclusive property ensures that once the consumer connection is closed, the queue is deleted
    temp_queue = channel.queue_declare(queue='', exclusive=True)

    # get name of temporary queue, bind the exchange and the queue
    queue_name = temp_queue.method.queue
    channel.queue_bind(exchange='logs', queue=queue_name)

    # define callback function
    def callback(ch, method, properties, body):
        message = body.decode("utf-8") 
        print('Successfully received message!')
        print(f'(queue={queue_name}, message={message})')
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # enter a never-ending loop that waits for data (messages) and runs callbacks whenever necessary
    print('Waiting for logs. . . To exit press CTRL+C')
    channel.start_consuming()


def main():
    receive_logs()


if __name__ == '__main__':
    main()
