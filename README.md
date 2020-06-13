# rabbitmq-playground
Playground for using RabbitMQ with Python (using Pika and Celery)  

To start a RabbitMQ instance in a Docker container, run this command:  

`docker run -d -p 5672:5672 -p 15672:15672 --hostname my-rabbitmq --name rabbitmq rabbitmq:3-management`  

5672 is the default port for RabbitMQ message broker, 15672 is the default port for RabbitMQ GUI  
RabbitMQ GUI can be accessed at [http://localhost:15672/#/](http://localhost:15672/#/), with the default username and password `guest:guest`  

