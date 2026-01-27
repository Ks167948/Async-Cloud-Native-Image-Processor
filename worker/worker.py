import redis
import json
import os
import time
import boto3
from PIL import Image
from io import BytesIO

# Redis Connection
redis_url = os.getenv("REDIS_URL", "redis://redis_db:6379")
# Handle the "rediss://" vs "redis://" issue automatically
if redis_url.startswith("rediss://"):
    # Secure connection for Cloud
    r = redis.from_url(redis_url, decode_responses=True, ssl_cert_reqs=None)
else:
    # Local connection
    r = redis.from_url(redis_url, decode_responses=True)

# AWS S3 Connection
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)
BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

print("Worker started. Listening for S3 jobs...")

while True:
    _, task_data = r.brpop('task_queue')
    task = json.loads(task_data)
    s3_key = task['key']
    
    print(f"Processing S3 file: {s3_key}...")
    
    try:
        # 1. Download image from S3 into memory (no hard drive needed!)
        response = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        image_data = response['Body'].read()
        
        # 2. Process image (Resize)
        img = Image.open(BytesIO(image_data))
        img.thumbnail((128, 128))
        
        # 3. Save processed image to a memory buffer
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0) # Rewind the buffer to the beginning
        
        # 4. Upload back to S3
        new_filename = f"processed/{os.path.basename(s3_key)}"
        s3.put_object(Bucket=BUCKET_NAME, Key=new_filename, Body=buffer, ContentType='image/jpeg')
        
        print(f"Success! Uploaded thumbnail to: {new_filename}")
        
    except Exception as e:
        print(f"Error processing {s3_key}: {e}")