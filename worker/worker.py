import redis
import json
import time
import os

# Connect to the same Redis container
redis_url = os.getenv("REDIS_URL", "redis://redis_db:6379")
r = redis.from_url(redis_url, decode_responses=True)

print("Worker started. Waiting for jobs...")

while True:
    # 1. 'brpop' blocks the code here until a new item appears in 'task_queue'
    # This is efficient; it doesn't spin the CPU while waiting.
    # It returns a tuple: (queue_name, data)
    _, task_data = r.brpop('task_queue')
    
    task = json.loads(task_data)
    filename = task['filename']
    
    print(f"Processing {filename}...")
    
    # 2. Simulate heavy processing (e.g., resizing, AI analysis)
    # In real life, you'd use PIL to resize here.
    time.sleep(5) 
    
    # 3. Rename the file to mark it as 'processed' (Simple proof of work)
    # Paths must match where we mounted the volume in Docker
    old_path = f"/app/uploads/{filename}"
    new_path = f"/app/uploads/processed_{filename}"
    
    try:
        os.rename(old_path, new_path)
        print(f"Success! Renamed to processed_{filename}")
    except FileNotFoundError:
        print("Error: File not found. Did volumes mount correctly?")