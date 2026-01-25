FROM python:3.9-slim

WORKDIR /app

# Install redis library
RUN pip install redis

COPY . .

# " -u" allows python print statements to show up in Docker logs immediately
CMD ["python", "-u", "worker.py"]