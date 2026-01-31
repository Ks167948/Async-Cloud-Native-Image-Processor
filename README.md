# 🚀 Scalable Async Image Processing Pipeline

![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white) ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) ![AWS S3](https://img.shields.io/badge/AWS_S3-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white) ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

> **A high-throughput, event-driven microservices architecture designed to handle CPU-intensive tasks without blocking the main application thread.**

---

## 🎥 System Demo

*Click the image above to watch the system process images in real-time across the hybrid cloud.*

---

## 🏗 System Architecture

The system decouples **Ingestion (I/O)** from **Processing (CPU)** using a distributed message queue. This ensures the API remains responsive (<50ms latency) even during heavy traffic spikes.

```mermaid
graph LR
    Client[User Client] -->|1. Upload Request| API[Node.js API Service]
    API -->|2. Stream File| S3[(AWS S3 Bucket)]
    API -->|3. Push Job| Redis[(Redis Queue)]
    Redis -->|4. Pull Task| Worker[Python Worker Service]
    Worker -->|5. Download File| S3
    Worker -->|6. Process & Re-upload| S3
