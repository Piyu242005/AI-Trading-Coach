<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeAuto&height=300&section=header&text=AI%20Trading%20Coach&fontSize=80&animation=fadeIn&fontAlignY=40&desc=A%20smart,%20memory-based%20AI%20coach%20that%20gives%20proven,%20explainable%20advice.&descAlignY=60&descSize=20" alt="AI Trading Coach Banner" />
</div>

## Overview
The AI Trading Coach is a robust API system designed to monitor streaming trading activity, profile participants, and deliver actionable coaching feedback. Built with persistent memory, it tracks and mitigates emotional and behavioral trading mistakes in real time.

## Problem Statement
Traders frequently suffer from psychological pitfalls such as overtrading, revenge trading, and tilt. Traditional analytical tools are focused entirely on post-trade PnL, completely ignoring the real-time emotional and behavioral lapses that lead to excessive drawdowns and blown accounts.

## Solution Approach
The system ingests streams of trades, processing the data through a deterministic heuristic engine to detect behavioral pathologies. Utilizing a persistent MongoDB memory architecture, it retrieves historical contexts to guarantee that the generated coaching advice is accurate, highly relevant, and free from hallucination.

## Features
- **Real-Time Signal Detection:** Autonomously identifies overtrading, revenge trading, and session tilt.
- **Streaming Coaching Engine:** Delivers token-by-token coaching feedback using Server-Sent Events (SSE).
- **Persistent Memory System:** Safely retains trade summaries and performance metrics across system restarts.
- **Anti-Hallucination Audit:** Actively cross-verifies all referenced sessions and trades against the core dataset.
- **Automated Evaluation Harness:** Validates detection accuracy (Precision, Recall, F1) against ground-truth labels.
- **Secure Authentication:** Implements JWT-based access controls to safeguard user-specific data.

## Tech Stack
- **Languages / Frameworks:** Python, FastAPI
- **Database:** MongoDB
- **Authentication:** PyJWT
- **Testing & Validation:** Pytest, Mongomock
- **Infrastructure:** Docker, Docker Compose

## Results / Impact
- **Algorithmic Accuracy:** Employs rule-based heuristics that achieve high precision and recall on ground-truth labeled datasets.
- **Business Value:** Decreases overall drawdown incidence by autonomously intervening during high-risk emotional states.
- **Explainability:** All coaching messages explicitly cite verifiable data points, including specific Session IDs and Trade IDs.

## Project Structure
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

## How to Run

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
- API Base URL: `http://localhost:8000`
- Swagger UI (Interactive API Docs): `http://localhost:8000/docs`

## Screenshots / Demo
*(Add screenshots of the Swagger UI, Evaluation Report HTML, or streaming endpoint in action here)*

## Future Improvements
- Implement deep learning models (e.g., LSTMs) for sequence anomaly detection.
- Integrate large language models (LLMs) for complex narrative generation over the existing deterministic engine.
- Introduce real-time WebSocket connections for live market data ingestion.

## Author
**Piyush Ramteke**
*Data Scientist | AI/ML Practitioner*
- GitHub: [Piyu242005](https://github.com/Piyu242005)
- LinkedIn: https://www.linkedin.com/in/piyu24/

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeAuto&height=150&section=footer" alt="Footer Animation" />
</div>