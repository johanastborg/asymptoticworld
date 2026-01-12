# 🌌 Asymptotic World
> *The AI-driven blog engine that writes, illustrates, and manages itself.*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-Platform-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Gemini](https://img.shields.io/badge/Powered_by-Gemini-8E75B2?style=for-the-badge)](https://deepmind.google/technologies/gemini/)

**Asymptotic World** is a fully autonomous, cloud-native blog engine. It doesn't just host content; it *creates* it. By leveraging advanced AI models for text and image generation, and integrating with real-time trends, it maintains a pulse on the world without human intervention.

---

## 🚀 Features

### 🧠 Deep Think Mode
Powered by **Gemini 3**, the engine's "Deep Think Mode" analyzes complex topics to generate insightful, well-structured blog posts. It doesn't just summarize; it synthesizes.

### 🍌 Nano Banana Imaging
Every post needs a cover. Our custom **Nano Banana** image generation engine creates unique, relevant, and visually striking header images for every single article, completely on the fly.

### 📈 Real-Time Trend Integration
Stuck for ideas? Asymptotic World isn't. It taps directly into the **Google Trends API** to identify what the world is talking about *right now* and generates content that matters.

### ☁️ True Cloud Native Architecture
- **Serverless Compute**: Runs on Google Cloud Run for effortless scaling.
- **Infinite Storage**: Uses **SQLite directly on Google Cloud Storage** via a custom `gcsfuse` mount implementation.
- **BigQuery Integration**: Includes a specialized Cloud Function acting as a Remote UDF to analyze HTML content directly within BigQuery.

---

## 🏗️ Architecture

The system consists of two main components:

### 1. The Core Application (`app/`)
A Flask-based web application that serves as the brain of the operation.
- **Endpoints**: RESTful API for listing posts, generating new content, and tracking stats.
- **Data Persistence**: Uses a unique setup where SQLite databases are stored in GCS buckets and mounted to the container using `gcsfuse` at runtime.
- **Entrypoint**: A custom `gcsfuse_run.sh` script handles the bucket mounting lifecycle before starting the Gunicorn server.

### 2. HTML Reader Function (`html-reader-func/`)
A dedicated Google Cloud Function designed for high-throughput data analysis.
- **Purpose**: Acts as a Remote UDF (User Defined Function) for BigQuery.
- **Functionality**: Reads raw HTML content from GCS URIs provided by BigQuery SQL queries, enabling massive-scale content analysis pipelines.

---

## 🛠️ Installation & Local Development

### Prerequisites
- Python 3.9+
- Docker (optional, for container testing)
- Google Cloud SDK (for deploying)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/asymptotic-world.git
   cd asymptotic-world
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   Set the following variables (create a `.env` file):
   ```bash
   export FLASK_APP=run.py
   export GOOGLE_CLOUD_PROJECT=your-project-id
   # Add keys for Gemini and other services as needed
   ```

4. **Run Locally**
   ```bash
   flask run
   ```

---

## 📦 Deployment

### Cloud Run (Core App)
The application is containerized and designed for Cloud Run. The `Dockerfile` and `gcsfuse_run.sh` handle the complex storage requirements.

```bash
# Build and Submit
gcloud builds submit --tag gcr.io/YOUR_PROJECT/asymptotic-world

# Deploy
gcloud run deploy asymptotic-world \
  --image gcr.io/YOUR_PROJECT/asymptotic-world \
  --execution-environment gen2 \
  --allow-unauthenticated \
  --set-env-vars BUCKET=your-sqlite-bucket
```

### Cloud Function (HTML Reader)
Deploy the BigQuery helper function:

```bash
cd html-reader-func
./deploy.sh
```

---

## 🔌 API Documentation

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/posts` | Retrieve a list of all blog posts (reverse chronological). |
| `POST` | `/posts/generate` | **Magic Button**. Triggers trend lookup, content writing, and image generation for a new post. |
| `POST` | `/stats/visit` | Records visitor statistics (page views, anonymous IPs). |

---

## 🤝 Contributing

We welcome contributions from humans and AIs alike!
1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/cool-new-thing`).
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

---

*Asymptotic World — Approaching the limit of infinite content.*
