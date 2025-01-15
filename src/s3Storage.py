import boto3
import os

def create_s3_client():
    """
    Create an S3 client.
    :rtype: :py:class:`boto3.client`
    :return: An S3 client
    """

    s3_endpoint = os.getenv("S3_ENDPOINT", "http://localhost:9000")
    s3_region = os.getenv("S3_REGION", "us-east-1")
    s3_access_key = os.getenv("S3_ACCESS_KEY", "minio")
    s3_secret_key = os.getenv("S3_SECRET", "password")
    return boto3.client(
        "s3",
        endpoint_url=s3_endpoint,
        region_name=s3_region,
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key,
    )


def download_image(s3_client, file_name, bucket_name):
    """
    Download an image from S3.
    :param s3_client: S3 client instance
    :param file_name: File name to download
    :param bucket_name: Bucket name
    :rtype: bytes
    :return: Image data as bytes
    """

    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    return response["Body"].read()


def replace_image(s3_client, file_name, bucket_name, image_data):
    """
    Replace an image in S3.
    :param s3_client: S3 client instance
    :param file_name: File name to replace
    :param bucket_name: Bucket name
    :param image_data: Image data to upload
    """

    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=image_data,
        ContentType="image/png",
    )