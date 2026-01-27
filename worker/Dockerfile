FROM python:3.9-slim

WORKDIR /app

# 1. Copy the requirements file first (for better caching)
COPY requirements.txt .

# 2. Install ALL dependencies (Redis, Boto3, Pillow, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of the code
COPY . .

# "-u" allows python print statements to show up in Docker logs immediately
CMD ["python", "-u", "worker.py"]