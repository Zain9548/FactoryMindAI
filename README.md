<img width="1920" height="1080" alt="Screenshot 2026-06-04 011449" src="https://github.com/user-attachments/assets/2da76f4b-7be4-4e1f-9435-00856a0bc684" />#
https://github.com/Zain9548/FactoryMindAI/blob/7941df8536951aa7f9a554a2774f7d5382ab2763/Demo%20Projects/Screenshot%202026-06-04%20011522.png
<img 
🏭
FactoryMind AI

## Industry 4.0 Predictive Maintenance Platform

FactoryMind AI is an end-to-end Industrial AI platform that helps predict machine failures, detect anomalies, monitor machine health in real time, and provide AI-powered maintenance recommendations using Retrieval-Augmented Generation (RAG).

---

# 📌 Project Overview

Unexpected machine failures can lead to production downtime, maintenance costs, and revenue loss.

FactoryMind AI solves this problem by combining:

* Machine Learning
* Anomaly Detection
* FastAPI
* Streamlit
* RAG Architecture
* ChromaDB
* LLM Integration

to create a complete Industrial Predictive Maintenance System.

---

# 🚀 Key Features

### Predictive Maintenance

* Predict machine failures before they happen
* Estimate machine risk levels
* Improve maintenance planning

### Anomaly Detection

* Detect abnormal machine behavior
* Identify unusual sensor patterns
* Generate early warning alerts

### Real-Time Monitoring

* Live machine sensor dashboard
* Machine health status
* Failure probability tracking

### Industrial AI Copilot

* Ask questions about machine maintenance
* Search machine manuals
* Get AI-powered maintenance recommendations

### RAG Pipeline

* PDF document ingestion
* Semantic search using embeddings
* Context-aware AI responses

---

# 🏗 System Architecture

Sensors / Simulated Data

↓

Feature Engineering

↓

XGBoost Failure Prediction Model

↓

Isolation Forest Anomaly Detection

↓

FastAPI Backend

↓

Streamlit Dashboard

↓

RAG System

↓

ChromaDB Vector Database

↓

OpenRouter LLM

↓

Industrial AI Copilot

---

# 📊 Dataset

Dataset Used:

AI4I 2020 Predictive Maintenance Dataset

Features:

* Air Temperature
* Process Temperature
* Rotational Speed
* Torque
* Tool Wear
* Machine Failure

---

# ⚙ Feature Engineering

Additional features created:

* Temperature Difference
* Wear Ratio
* Torque Stress
* Thermal Stress
* Load Index

These features improved model understanding and prediction quality.

---

# 🤖 Machine Learning Models

## Failure Prediction

Model:

XGBoost Classifier

Purpose:

Predict whether a machine is likely to fail.

---

## Anomaly Detection

Model:

Isolation Forest

Purpose:

Detect unusual machine behavior.

---

# 🧠 RAG-Based Industrial AI Copilot

The AI Copilot allows users to ask maintenance-related questions.

Example Questions:

* Why machine overheating?
* How to reduce tool wear?
* What causes spindle failure?
* How to prevent machine downtime?

Workflow:

User Question

↓

Embedding Generation

↓

ChromaDB Retrieval

↓

Relevant PDF Chunks

↓

LLM Processing

↓

Final Industrial Answer

---

# 🛠 Tech Stack

### Programming

* Python

### Machine Learning

* XGBoost
* Scikit-Learn

### Backend

* FastAPI

### Frontend

* Streamlit

### Vector Database

* ChromaDB

### Embeddings

* Sentence Transformers

### LLM

* OpenRouter
* Llama 3 / Mistral

### Visualization

* Plotly
* Pandas

---

# 📂 Project Structure

FactoryMindAI/

├── backend/

├── frontend/

├── rag/

├── models/

├── knowledge_base/

├── vector_db/

├── requirements.txt

├── README.md

└── .gitignore

---

# ▶ Installation

Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/FactoryMind-AI.git
```

Move into project

```bash
cd FactoryMind-AI
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows

```bash
venv\Scripts\activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Run Backend

```bash
cd backend

uvicorn app:app --reload
```

Runs on:

```text
http://127.0.0.1:8000
```

---

# ▶ Run RAG API

```bash
cd rag

uvicorn ask:app --reload --port 9000
```

Runs on:

```text
http://127.0.0.1:9000
```

Swagger Docs:

```text
http://127.0.0.1:9000/docs
```

---

# ▶ Run Frontend

```bash
cd frontend

streamlit run dashboard.py
```

---

# 📈 Dashboard Features

* Failure Probability
* Machine Health Score
* Anomaly Alerts
* Live Sensor Monitoring
* AI Copilot Chat
* Industrial Analytics

---

# 🎯 Results

FactoryMind AI successfully combines:

* Predictive Maintenance
* Anomaly Detection
* Real-Time Monitoring
* RAG-Based Question Answering
* Industrial AI Assistance

into a single Industry 4.0 platform.

---

# The frontend was successfully deployed on Streamlit Cloud. However, the backend APIs were running locally because I had exhausted the free deployment limits on Render and Railway. Due to this, the cloud-hosted frontend could not connect to the backend APIs. On my local machine, the complete system works end-to-end, including FastAPI backend, machine learning models, and the RAG-based AI copilot.

# 🔮 Future Improvements

* Kafka Streaming
* IoT Sensor Integration
* Remaining Useful Life (RUL) Prediction
* AWS Deployment
* Multi-Machine Monitoring
* WhatsApp & Email Alerts

---

# 👨‍💻 Author

Mohd Ajeem

Aspiring Data Scientist & Machine Learning Engineer

Skills:

Python | Machine Learning | FastAPI | Streamlit | RAG | Data Science
