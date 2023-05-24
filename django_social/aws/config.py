import boto3
from botocore.config import Config

AWS_STORAGE_BUCKET_NAME = 'images'


def setup_aws():
    boto3.setup_default_session()

    s3 = boto3.client(
        's3',
        region_name='us-east-1',
        endpoint_url='http://localstack:4566',  # LocalStack endpoint for S3
        aws_access_key_id='dummy',  # Dummy credentials for local development
        aws_secret_access_key='dummy',
        config=Config(signature_version='v4', s3={'addressing_style': 'path'})
    )
    s3.create_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)

    ses = boto3.client(
        'ses',
        region_name='us-east-1',
        endpoint_url='http://localstack:4566',  # LocalStack endpoint for SES
        aws_access_key_id='dummy',  # Dummy credentials for local development
        aws_secret_access_key='dummy',
        config=Config(signature_version='v4', s3={'addressing_style': 'path'})
    )
    ses.verify_email_identity(EmailAddress='noreply@example.com')

    return s3, ses
