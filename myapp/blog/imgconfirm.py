import boto3
import os

session = boto3.Session(
    aws_access_key_id= os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=os.environ.get("AWS_REGION")  # 예: 'us-east-1'
)
s3_client = session.client('s3')
bucket_name = os.environ.get("AWS_STORAGE_BUCKET_NAME")
img_objects = s3_client.list_objects(Bucket=bucket_name)

