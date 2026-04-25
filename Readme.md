<div align="center">
  <h1>📊 AI Trading Coach</h1>
  <p><b>A smart, memory-based AI coach that gives proven, explainable advice.</b></p>
</div>

<div align="center">
  
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)

</div>

---

## 📖 Case Study Overview
The **AI Trading Coach** is a robust API system designed to monitor streaming trading activity, profile participants, and deliver actionable coaching feedback. Built with persistent memory, it tracks and mitigates emotional and behavioral trading mistakes in real time.

> **Our Mission:** To provide traders with a smart, context-aware coaching system that intervenes during high-risk emotional states, reducing drawdowns and improving long-term profitability.

---

## 🛑 The Challenge (Problem Statement)
Traders frequently suffer from psychological pitfalls such as:
- 📉 **Overtrading:** Forcing trades when no clear edge exists.
- 😡 **Revenge Trading:** Trying to win back losses immediately.
- 🤯 **Tilt:** Trading emotionally due to successive losses.

Traditional analytical tools are focused entirely on post-trade PnL, completely ignoring the real-time emotional and behavioral lapses that lead to excessive drawdowns and blown accounts.

---

## 💡 The Solution
The system ingests streams of trades, processing the data through a **deterministic heuristic engine** to detect behavioral pathologies. Utilizing a **persistent MongoDB memory architecture**, it retrieves historical contexts to guarantee that the generated coaching advice is accurate, highly relevant, and **free from hallucination**.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🚀 **Real-Time Signal Detection** | Autonomously identifies overtrading, revenge trading, and session tilt. |
| 📡 **Streaming Coaching Engine** | Delivers token-by-token coaching feedback using Server-Sent Events (SSE). |
| 🧠 **Persistent Memory System** | Safely retains trade summaries and performance metrics across system restarts. |
| 🔍 **Anti-Hallucination Audit** | Actively cross-verifies all referenced sessions and trades against the core dataset. |
| 📊 **Automated Evaluation** | Validates detection accuracy (Precision, Recall, F1) against ground-truth labels. |
| 🔒 **Secure Authentication** | Implements JWT-based access controls to safeguard user-specific data. |

---

## 🛠️ Tech Stack & Architecture

- **Languages / Frameworks:** Python, FastAPI
- **Database:** MongoDB
- **Authentication:** PyJWT
- **Testing & Validation:** Pytest, Mongomock
- **Infrastructure:** Docker, Docker Compose

### 📂 Project Structure
```text
nevup-api/
├── app/
│   ├── routes/          # API endpoints (Coaching, Memory, Profiling, Audit)
│   ├── services/        # Core business logic and dataset utilities
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # Pydantic schemas for data validation
│   └── auth.py          # JWT authentication utilities
├── data/                # Seed datasets with ground truth labels
├── tests/               # Pytest suite for end-to-end API validation
├── docker-compose.yml   # Container orchestration configuration
├── Dockerfile           # Application container image
└── requirements.txt     # Python dependencies
```

---

## 📈 Results & Impact

- 🎯 **Algorithmic Accuracy:** Employs rule-based heuristics that achieve high precision and recall on ground-truth labeled datasets.
- 💰 **Business Value:** Decreases overall drawdown incidence by autonomously intervening during high-risk emotional states.
- 🗣️ **Explainability:** All coaching messages explicitly cite verifiable data points, including specific Session IDs and Trade IDs.

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/Piyu242005/AI-Trading-Coach.git
cd AI-Trading-Coach/nevup-api
```

**2. Run with Docker (Recommended)**
```bash
docker-compose up --build
```

**3. Run locally (Alternative)**
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**4. Access the Application**
- **API Base URL:** `http://localhost:8000`
- **Swagger UI (Interactive API Docs):** `http://localhost:8000/docs`

---

## 📸 Screenshots / Demo
> *(Add screenshots of the Swagger UI, Evaluation Report HTML, or streaming endpoint in action here)*

---

## 🔮 Future Improvements
- [ ] Implement deep learning models (e.g., LSTMs) for sequence anomaly detection.
- [ ] Integrate large language models (LLMs) for complex narrative generation over the existing deterministic engine.
- [ ] Introduce real-time WebSocket connections for live market data ingestion.

---

## 👨‍💻 Author
**Piyush Ramteke**  
*Data Scientist | AI/ML Practitioner*  
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Piyu242005)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/piyu24/)

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeAuto&height=150&section=footer" alt="Footer Animation" />
</div>