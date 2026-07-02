
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import os

load_dotenv(override=True)

AWS_ACCESS_KEY_ID = os.getenv("Access_key")
AWS_SECRET_ACCESS_KEY = os.getenv("Secret_access_key")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("s3name")