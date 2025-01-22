import logging
import os
import pika
from pika.exceptions import AMQPConnectionError
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class RabbitMQClient:

    def __init__(self):
        self.rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        self.rabbitmq_port = os.getenv("RABBITMQ_PORT", 5672)
        self.rabbitmq_user = os.getenv("RABBITMQ_USER", "user")
        self.rabbitmq_password = os.getenv("RABBITMQ_PASSWORD", "password")
        logging.info(f"Connecting to RabbitMQ at {self.rabbitmq_host}:{self.rabbitmq_port} as {self.rabbitmq_user}")
        self.connection = None
        self.channel = None
        self.connection_with_retries()

    def connection_with_retries(self, max_retries=10, initial_delay=5):
        """
        Attempt to establish a RabbitMQ connection with retry logic.
        """
        retries = 0
        while retries < max_retries:
            try:
                logging.info(f"Attempting to connect to RabbitMQ... ({retries + 1}/{max_retries})")

                credentials = pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_password)
                parameters = pika.ConnectionParameters(
                    host=self.rabbitmq_host,
                    port=self.rabbitmq_port,
                    credentials=credentials,
                    heartbeat=30,  # Send heartbeat to keep connection alive
                    blocked_connection_timeout=300,  # Timeout for blocked connections
                    retry_delay=5
                )

                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                logging.info("Connected to RabbitMQ successfully!")
                return

            except AMQPConnectionError as e:
                logging.error(f"RabbitMQ connection failed: {e}. Retrying in {initial_delay} seconds...")
                time.sleep(initial_delay)
                retries += 1

        raise Exception("Could not connect to RabbitMQ after multiple retries.")

    def ensure_connection(self):
        """
        Ensure that the RabbitMQ connection is established. If not, retry connecting.
        """
        if self.connection is None or self.connection.is_closed:
            logging.info("RabbitMQ connection lost. Reconnecting...")
            self.connection_with_retries()

    def consume_messages(self, queue, callback):
        """
        Consume messages from a RabbitMQ queue.
        """
        self.ensure_connection()
        self.channel.queue_declare(queue=queue, durable=True) # Ensure that the queue exists
        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=False)
        logging.info(f"Waiting for messages in {queue}...")
        self.channel.start_consuming()

    def close_connection(self):
        """
        Close the RabbitMQ connection.
        """
        if self.connection and self.connection.is_open:
            self.connection.close()
            logging.info("RabbitMQ connection closed.")
