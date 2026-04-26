<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeAuto&height=150&section=header&text=AI%20Trading%20Coach&fontSize=50" alt="Header Animation"/>
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
The **AI Trading Coach** is a robust backend system designed to monitor streaming trading activity, profile participants, and deliver actionable coaching feedback. Built with persistent memory, it tracks and mitigates emotional and behavioral trading mistakes (Overtrading, Revenge Trading, FOMO) in real time.

---

## 🏗️ System Architecture
The system follows a modern, event-driven backend design:
1. **Ingestion Layer:** Accepts streaming trade data via FastAPI endpoints.
2. **Deterministic Engine:** Analyzes trade sequences and emotional flags to trigger behavioral pathologies using explicit heuristics.
3. **Memory Store:** Persists user statistics and session data in MongoDB, giving the AI "context" across time.
4. **Coaching Engine:** Dispatches personalized advice via Server-Sent Events (SSE) based on verified memory constraints.

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI (Async web framework)
- **Database:** MongoDB (Document-oriented memory persistence)
- **Real-Time Data:** Server-Sent Events (SSE)
- **Authentication:** PyJWT
- **Containerization:** Docker & Docker Compose

---

## 🚀 Deployment
The application is live and accessible at:  
👉 **[https://ai-trading-coach-2vao.onrender.com/](https://ai-trading-coach-2vao.onrender.com/)**

> Note: Access `/docs` at the deployment URL to test the interactive Swagger UI.

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
| :--- | :---: | :--- |
| `/api/auth/token` | `POST` | Generates a JWT for secure access. |
| `/api/ingest` | `POST` | Receives raw trade data and updates the user profile. |
| `/api/coach/stream` | `GET` | Streams tokenized coaching feedback via SSE. |
| `/api/memory/{userId}` | `GET` | Retrieves the historical context for a specific user. |
| `/api/audit` | `GET` | Verifies coaching outputs against database records to prevent hallucination. |

### 📝 Example Request / Response

**Ingest Trade (POST `/api/ingest`)**
```json
// Request payload
{
  "userId": "f412f236-4edc-47a2-8f54-8763a6ed2ce8",
  "sessionId": "4f39c2ea-8687-41f7-85a0-1fafd3e976df",
  "outcome": "loss",
  "revengeFlag": true,
  "emotionalState": "anxious"
}
```

**Coaching Stream (GET `/api/coach/stream`)**
```text
data: {"token": "Warning:"}
data: {"token": " Revenge"}
data: {"token": " trading"}
data: {"token": " detected."}
```

---

## 📊 Evaluation Report
To prove the system's ability to accurately classify pathologies, we developed an evaluation pipeline measuring **Precision**, **Recall**, and **F1 Score**.

- **Precision:** How many flagged pathologies were actually correct.
- **Recall:** How many actual pathologies the system successfully caught.
- **F1 Score:** The harmonic mean of Precision and Recall.

*Our heuristic-based approach achieved a highly accurate score, particularly at identifying overtrading and revenge trading by isolating specific session volume thresholds and loss-recovery patterns.*

### 🛠️ How to Reproduce Results
We have included a reproducible evaluation script inside the repository:
1. Ensure dependencies are installed (`pip install -r requirements.txt`).
2. Run the script:
   ```bash
   python evaluate.py
   ```
3. The metrics will be outputted to the console and saved to `reports/classification_report.json`.

---

## 💻 Running Locally

### 🐳 Method 1: Using Docker (Recommended)
1. Clone the repository:
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
1. Clone the repository and navigate to `nevup-api`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

---

## 📸 Screenshots / Demo

![Live Deployment URL](assets/Live%20Deployment%20URL.png)

---

## 👨‍💻 Author
**Piyush Ramteke**  
*Data Scientist | AI/ML Practitioner*  
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Piyu242005)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/piyu24/)

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeAuto&height=150&section=footer" alt="Footer Animation" />
</div>