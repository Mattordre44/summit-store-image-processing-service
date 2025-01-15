import json
import os
from imageProcessing import is_background_uniform, remove_background
from rabbitMQ import create_rabbitmq_client
from s3Storage import create_s3_client, download_image, replace_image


s3_client = create_s3_client()
rabbitmq_client = create_rabbitmq_client()


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

def callback(ch, method, properties, body):
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
        print(f"Received message: {message}")
        file_name = message["fileName"]
        bucket_name = message["bucketName"]

        # Download the image from S3
        image_data = download_image(s3_client, file_name, bucket_name)

        # Process the image
        image_data = process_image(image_data)

        # Replace the image to S3
        replace_image(s3_client, file_name, bucket_name, image_data)

        # Acknowledge the message after successful processing
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        # Reject the message
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
     

def main():

    queue_name = os.getenv("QUEUE_NAME", "image.processing.background")
   
    channel = rabbitmq_client.channel()

    # Declare the queue (ensure it exists)
    channel.queue_declare(queue=queue_name, durable=True)

    print(f"Waiting for messages in {queue_name}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


if __name__ == "__main__":
    main()