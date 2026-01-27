🚀 AWS-Powered Async Image Processing Pipeline
A production-ready microservices architecture that decouples high-throughput I/O from heavy computation using a distributed queue and cloud object storage.

[Insert Screenshot of your Terminal Logs Here]

🏗 System Architecture
The system handles heavy image processing tasks asynchronously to ensure the API remains non-blocking and responsive.

Code snippet
graph LR
    User(Client) -->|1. Upload Image| API[Node.js API]
    API -->|2. Stream to Cloud| S3[(AWS S3 Bucket)]
    API -->|3. Push Job| Redis[(Redis Queue)]
    Redis -->|4. Pull Job| Worker[Python Worker]
    Worker -->|5. Download & Process| S3
    Worker -->|6. Upload Thumbnail| S3
🌟 Key Features
Event-Driven Architecture: Decoupled the API (Producer) from the Worker (Consumer) using Redis.

Cloud Storage Integration: Implemented AWS S3 for secure, scalable object storage, solving the "shared state" problem in distributed systems.

Polyglot Microservices:

Service A (Node.js): Handles HTTP requests and S3 streaming.

Service B (Python): Performs CPU-intensive image manipulation (Pillow).

Containerization: Fully Dockerized environment ensuring identical behavior in Dev and Prod.

🛠 Tech Stack
Languages: Node.js (Express), Python 3.9

Cloud Services: AWS S3 (Storage), Upstash (Serverless Redis)

DevOps: Docker, Docker Compose

Libraries: @aws-sdk/client-s3, multer-s3, boto3, Pillow

🚀 How to Run
Prerequisites: Docker Desktop & AWS Credentials.

Clone the Repo

Bash
git clone https://github.com/yourusername/async-processor.git
cd async-processor
Configure Environment Update docker-compose.yml with your keys (or use a .env file):

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_BUCKET_NAME

AWS_REGION

Start the Cluster

Bash
docker-compose up --build
Test It

Go to http://localhost:3000.

Upload an image.

Check your AWS S3 Bucket for the processed/ folder!
