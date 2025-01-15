import os
import pika

def create_rabbitmq_client():
    """
    Create a RabbitMQ client.
    :rtype: :py:class:`pika.BlockingConnection`
    :return: A RabbitMQ client
    """

    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
    rabbitmq_port = os.getenv("RABBITMQ_PORT", 5672)
    rabbitmq_user = os.getenv("RABBITMQ_USER", "user")
    rabbitmq_password = os.getenv("RABBITMQ_PASSWORD", "password")
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host, 
            port=rabbitmq_port,
            credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
        )
    )