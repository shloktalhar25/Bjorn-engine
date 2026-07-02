import boto3
from botocore.exceptions import ClientError
from pathlib import Path

from config.settings import (
    AWS_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    BUCKET_NAME,
)

BASE_DIR = Path(__file__).resolve().parent.parent

def upload_file_to_s3(filepath=None, bucket_name=None, object_name=None):
    if filepath is None:
        filepath = BASE_DIR / "data" / "processed" / "listings_clean.parquet"
    else:
        filepath = Path(filepath)

    if bucket_name is None:
        bucket_name = BUCKET_NAME

    if object_name is None:
        object_name = "processed/listings_clean.parquet"

    print(f"Uploading {filepath} to S3 bucket {bucket_name} as {object_name}...")

    if not filepath.exists():
        raise FileNotFoundError(f"File to upload not found: {filepath}")

    # Initialize S3 client with config credentials if provided
    s3_params = {}
    if AWS_ACCESS_KEY_ID:
        s3_params["aws_access_key_id"] = AWS_ACCESS_KEY_ID
    if AWS_SECRET_ACCESS_KEY:
        s3_params["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    if AWS_REGION:
        s3_params["region_name"] = AWS_REGION

    s3_client = boto3.client("s3", **s3_params)

    try:
        s3_client.upload_file(str(filepath), bucket_name, object_name)
        print(f"File {filepath} has been successfully uploaded to s3://{bucket_name}/{object_name}")
        return True
    except ClientError as e:
        print(f"Failed to upload file to S3: {e}")
        raise e

if __name__ == "__main__":
    upload_file_to_s3()