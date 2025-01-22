import json
import logging
import os
from imageProcessing import is_background_uniform, remove_background
from rabbitMQ import RabbitMQClient
from s3Storage import S3Client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

s3_client = S3Client()
rabbitmq_client = RabbitMQClient()


def process_image(image_data):
    """
    Process an image by removing the background if it is uniform.
    :param image_data: Image data as bytes
    :rtype: bytes
    :return: Processed image data
    """
    if is_background_uniform(image_data):
        return remove_background(image_data)
    else:
        return image_data


def callback(ch, method, _, body):
    """
    Callback function triggered when a message is received.
    :param ch: Channel
    :param method: Method frame
    :param properties: Properties
    :param body: Message body
    """
    try:
        # Deserialize the JSON message
        message = json.loads(body.decode())
        logging.info(f"Received message: {message}")
        file_name = message["fileName"]
        bucket_name = message["bucketName"]

        # Download the image from S3
        image_data = s3_client.download_image(file_name, bucket_name)

        # Process the image
        image_data = process_image(image_data)

        # Replace the image to S3
        s3_client.replace_image(file_name, bucket_name, image_data)

        # Acknowledge the message after successful processing
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        # Reject the message
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
     

def main():
    queue_name = os.getenv("QUEUE_NAME", "image.processing.background")
    rabbitmq_client.consume_messages(queue_name, callback)


main()