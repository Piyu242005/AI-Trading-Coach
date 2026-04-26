<div align="center">
<!-- Animated Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=AI%20Trading%20Coach&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=32&desc=Behavioral%20AI%20for%20Smart%20Trading&descSize=18&descAlignY=52" width="100%" />

</div>

<div align="center">
  <p><b>A smart, memory-based AI system that delivers proven, explainable trading advice.</b></p>
  
  ![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
  ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
  ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb)
  ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)

  <br>
  <strong>🔗 <a href="https://ai-trading-coach-2vao.onrender.com/">Live Deployment</a></strong>
</div>

---

## 🎯 Overview
The **AI Trading Coach** is a robust backend system designed to monitor streaming trading activity, profile participants, and deliver actionable coaching feedback. Built with persistent memory, it tracks and mitigates emotional and behavioral trading mistakes in real time. 

It now comprehensively detects **all 9 core behavioral pathologies**: Overtrading, Revenge Trading, Session Tilt, FOMO Entries, Plan Non-Adherence, Premature Exit, Loss Running, Time of Day Bias, and Position Sizing Inconsistency.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🚀 **Comprehensive Detection** | Identifies all 9 behavioral pathologies using rigorous, deterministic heuristics. |
| 📡 **Streaming Coaching Engine** | Delivers token-by-token coaching feedback using Server-Sent Events (SSE). |
| 🧠 **Persistent Memory System** | Safely retains trade summaries and performance metrics across system restarts via MongoDB. |
| 🔍 **Anti-Hallucination Audit** | Actively cross-verifies all referenced sessions and trades against the core database. |
| 📊 **Automated Evaluation** | Validates detection accuracy (Precision, Recall, F1) using a unified, reproducible engine. |
| 🔒 **Strict JWT Authentication** | Enforces HS256 JWT validation matching user identity to `token.sub` for secure multi-tenancy. |

---

## 🏗️ System Flow & Architecture
The system follows a modern, event-driven backend flow:
1. **Profiling & Ingestion:** Streaming trade data is ingested via FastAPI and evaluated against deterministic heuristic rules.
2. **Memory Persistence:** User statistics, context, and detected signals are persisted securely in MongoDB.
3. **Coaching Delivery:** Personalized advice is streamed via Server-Sent Events (SSE). All advice explicitly cites verified `sessionId` and `tradeId` evidence to guarantee zero hallucination.
4. **Evaluation & Audit:** The system continually self-evaluates, exposing endpoints to verify data integrity and classification accuracy.

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI (Async web framework)
- **Database:** MongoDB (Document-oriented memory persistence)
- **Real-Time Data:** Server-Sent Events (SSE)
- **Authentication:** PyJWT (Strict HS256 Signature Validation)
- **Containerization:** Docker & Docker Compose

---

## 📂 Project Structure
```text
nevup-api/
├── app/
│   ├── routes/          # API endpoints (Coaching, Memory, Profiling, Audit, Evaluation)
│   ├── services/        # Core business logic and dataset utilities
│   ├── main.py          # FastAPI application entry point + DB Healthcheck
│   ├── models.py        # Pydantic schemas for data validation
│   └── auth.py          # JWT authentication utilities
├── data/                # Seed datasets with ground truth labels
├── tests/               # Pytest suite for end-to-end API validation
├── evaluate.py          # Unified CLI script for generating the classification report
├── docker-compose.yml   # Container orchestration configuration
└── Dockerfile           # Application container image
```

---

## 🚀 Deployment
The application is live and accessible at:  
👉 **[https://ai-trading-coach-2vao.onrender.com/](https://ai-trading-coach-2vao.onrender.com/)**

- Interactive Swagger UI: `https://ai-trading-coach-2vao.onrender.com/docs`
- Live Evaluation Report: `https://ai-trading-coach-2vao.onrender.com/evaluation/report?format=html`

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
| :--- | :---: | :--- |
| `/api/auth/token` | `POST` | Generates a JWT for secure access. |
| `/api/ingest` | `POST` | Receives raw trade data and updates the user profile. |
| `/api/coach/stream` | `POST` | Streams tokenized, evidence-based coaching feedback via SSE. |
| `/api/memory/{userId}` | `GET` | Retrieves the historical context for a specific user. |
| `/audit` | `POST` | Verifies coaching outputs against database records to prevent hallucination. |
| `/evaluation/report` | `GET` | Returns the dynamic Precision/Recall/F1 classification report (JSON/HTML). |
| `/health` | `GET` | Performs a live database connectivity ping. |

---

## 📈 Results & Impact
- 🎯 **Algorithmic Accuracy:** Employs rule-based heuristics that achieve realistic precision and recall across all 9 ground-truth pathologies.
- 💰 **Business Value:** Decreases overall drawdown incidence by autonomously intervening during high-risk emotional states.
- 🗣️ **Zero Hallucination:** All coaching messages explicitly cite verifiable data points, guaranteeing explainability.

---

## 📊 Unified Evaluation Report
To prove the system's ability to accurately classify pathologies, we developed a unified evaluation pipeline measuring **Precision**, **Recall**, and **F1 Score** across all 9 target labels. 

The evaluation logic is shared identically between the API endpoint and the CLI script to ensure absolute consistency and reproducibility.

### 🛠️ How to Reproduce Results
1. Ensure dependencies are installed (`pip install -r requirements.txt`).
2. Run the unified evaluation script:
   ```bash
   python evaluate.py
   ```
3. The metrics will be outputted to the console and saved locally to `reports/classification_report.json`.

---

## 💻 Running Locally

### 🐳 Method 1: Using Docker (Recommended)
1. Clone the repository and navigate to `nevup-api`:
   ```bash
   git clone https://github.com/Piyu242005/AI-Trading-Coach.git
   cd AI-Trading-Coach/nevup-api
   ```
2. Build and run the containers:
   ```bash
   docker-compose up --build -d
   ```
3. Access the API at `http://localhost:8000/docs`

### 🐍 Method 2: Manual Setup
1. Clone the repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

---

## 👨‍💻 Author
**Piyush Ramteke**  
*Data Scientist | AI/ML Practitioner*  
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Piyu242005)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/piyu24/)

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeAuto&height=150&section=footer" alt="Footer Animation" />
</div>