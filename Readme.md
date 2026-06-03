
<div align="center">

<!-- Animated Hero Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=10,20,30&height=220&section=header&text=AI%20Trading%20Coach&fontSize=60&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Full-Stack%20Behavioral%20AI%20for%20Financial%20Decision%20Support&descSize=22&descAlignY=55" width="100%" />

<br />

[![Deployment](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=vercel&logoColor=white)](https://ai-trading-coach-2vao.onrender.com/)
[![Documentation](https://img.shields.io/badge/Swagger-API-blue?style=for-the-badge&logo=swagger&logoColor=white)](https://ai-trading-coach-2vao.onrender.com/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![React 19](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)

<p align="center">
  <b>A production-grade SaaS platform providing reliable, explainable trading coaching through RAG, persistent memory, and a ChatGPT-style conversational interface.</b>
</p>

</div>

<br />

# AI Trading Coach
AI-Powered Trading Intelligence, Portfolio Analytics & Financial Decision Support System

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-111827?style=for-the-badge&logo=tensorflow&logoColor=white)](#)
[![OpenAI](https://img.shields.io/badge/OpenAI-0F172A?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-31648C?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-0DB7ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)

## Overview
AI Trading Coach is a production-grade Trading Intelligence Platform that combines behavioral AI, portfolio analytics, and market intelligence to improve financial decision making. It delivers personalized coaching, risk-aware insights, and portfolio diagnostics through a clean Streamlit experience backed by a FastAPI service.

Core platform pillars:
- AI Coaching that explains decisions in plain language
- Portfolio Analytics with risk, performance, and allocation views
- Market Intelligence for trends, volatility, and opportunity detection
- Trading Journal Analytics to improve repeatable strategy execution
- Personalized Financial Insights grounded in user trading history

## Key Features
### AI Trading Coach
- Conversational AI assistant for trade questions and guidance
- Market explanations and context-aware coaching
- Portfolio-aware recommendations and risk feedback

### Portfolio Intelligence
- Asset allocation analysis and sector exposure
- Risk scoring and behavioral discipline signals
- Performance tracking and equity curve analysis
- Diversification diagnostics and drawdown insights

### Market Analytics
- Technical indicator snapshots and moving averages
- Trend analysis and momentum tracking
- Volatility monitoring and regime detection
- Opportunity detection from historical performance

### Trading Journal
- Trade tracking with notes, confidence, and outcomes
- Strategy evaluation with win rate and PnL summaries
- Behavioral analysis for overtrading, tilt, and revenge patterns

## System Architecture
```mermaid
flowchart TD
    user[User] --> streamlit[Streamlit Frontend]
    streamlit --> fastapi[FastAPI Backend]
    fastapi --> ai[AI Engine]
    ai --> analytics[Analytics Engine]
    analytics --> db[(Database)]
```

## 🏗️ System Architecture & Deployment

The AI Trading Coach utilizes a highly decoupled, modern microservices architecture optimized for latency and scalability.

**Deployment Stack:**
*   **Frontend**: React + Vite + Tailwind CSS (Deployed on **Vercel**)
*   **Backend**: FastAPI + Python 3.10 (Deployed on **Render**)
*   **Database**: MongoDB (Hosted on **MongoDB Atlas**)

<div align="center">
  <img src="./Research_Submission/📊%20Figures%20%26%20Diagrams/1.%20system%20architecture.png" alt="System Architecture" width="100%" />
  <p><i>Figure 1: End-to-end data flow from trade ingestion to streaming coaching delivery.</i></p>
</div>

### 🔄 Workflow Pipeline
1.  **Data Ingestion Layer**: Raw trade streams are ingested and normalized via FastAPI.
2.  **Heuristic Engine**: Deterministic rules identify behavioral signals.
3.  **Contextual Memory**: Signals are stored in MongoDB Atlas to build long-term profiles.
4.  **Inference & Verification**: The LLM generates coaching, which is then audited for factual accuracy.
5.  **Streaming Delivery**: Validated advice is pushed to the React client via Server-Sent Events (SSE).

---

## 🛠️ Tech Stack

<div align="center">

| Frontend | Backend | Database & Infrastructure |
| :---: | :---: | :---: |
| ![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB) | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | ![MongoDB Atlas](https://img.shields.io/badge/MongoDB_Atlas-47A248?style=flat&logo=mongodb&logoColor=white) |
| ![Vite](https://img.shields.io/badge/Vite-B73BFE?style=flat&logo=vite&logoColor=FFD62E) | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi&logoColor=white) | ![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat&logo=vercel&logoColor=white) |
| ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white) | ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=chainlink&logoColor=white) | ![Render](https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white) |
| ![Zustand](https://img.shields.io/badge/Zustand-443E38?style=flat&logo=react&logoColor=white) | ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white) | ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=github-actions&logoColor=white) |

</div>


## Screenshots
Placeholders for portfolio visuals. Replace with real screenshots once available.

- Dashboard: `assets/screenshots/dashboard.png`
- AI Coach: `assets/screenshots/ai-coach.png`
- Portfolio Analytics: `assets/screenshots/portfolio-analytics.png`
- Trading Journal: `assets/screenshots/trading-journal.png`

## Installation Guide
### Prerequisites
- Python 3.10+
- Node.js 20+ (optional, for React frontend)
- Docker (optional)

### Local Backend Setup
```bash
git clone https://github.com/Piyu242005/AI-Trading-Coach.git
cd AI-Trading-Coach
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Streamlit Frontend
```bash
cd frontend-streamlit
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Optional React Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker (Full Stack)
```bash
docker-compose up --build
```

## Project Structure
```text
AI-Trading-Coach/
├── app/                    # FastAPI application
│   ├── routes/             # API routes (coaching, profiling, discipline, memory)
│   ├── services/           # Heuristics and AI logic
│   ├── auth.py             # Auth helpers
│   ├── database.py         # Dataset loading
│   ├── main.py             # FastAPI entrypoint
│   └── models.py           # Pydantic models
├── frontend/               # React + Vite client (optional)
├── frontend-streamlit/     # Streamlit client (primary demo)
│   ├── app.py
│   └── requirements.txt
├── data/                   # Sample datasets
├── assets/                 # Images and static assets
├── tests/                  # Pytest suite
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── requirements-dev.txt
```

## GitHub Actions
Continuous Integration runs on every push and pull request:
- Backend linting and formatting with Ruff
- Pytest execution for API correctness
- Frontend lint and build validation for the React client

## Future Roadmap
- Agentic AI Trading Assistant with multi-step reasoning
- Sentiment analysis across news and social signals
- RAG-based market research and thesis generation
- Portfolio optimization engine with constraints
- Explainable AI insights for every recommendation
- Real-time market data integration

## Why This Project Matters
This repository demonstrates end-to-end capability across:
- AI Engineering and model orchestration
- Machine Learning and behavioral analytics
- Financial analytics and portfolio intelligence
- Full-stack delivery with FastAPI and Streamlit
- Data science workflows and production-ready DevOps


## 📸 Visual Showcase

<details>
<summary><b>Click to expand screenshots</b></summary>

### 🏗️ Workflow Diagram
<img src="./Research_Submission/📊%20Figures%20%26%20Diagrams/2.%20workflow%20diagram.png" width="100%" />

### 🚀 System Pipeline
<img src="./Research_Submission/📊%20Figures%20%26%20Diagrams/3.%20system%20pipeline.png" width="100%" />

### 🖥️ API Response Preview
<img src="./assets/api_preview.png" width="100%" />

### 📈 Evaluation Charts
<img src="./Research_Submission/📊%20Figures%20%26%20Diagrams/4.%20evaluation%20charts.png" width="100%" />

</details>

---

## 📜 Research & Publications

This project is part of a broader study on **Behavioral Pathology in Financial Markets**.

*   **Preprint**: *Explainable Behavioral AI Systems for Trading Decision Support* (In Review)
*   **Key Findings**: Demonstrated a **100% detection rate** for time-based and volume-based overtrading patterns.
*   **Methodology**: Hybrid heuristic-LLM approach for high-precision coaching.

---

## 🔮 Future Roadmap
- [ ] **Multimodal AI Integration**: Analyzing trader sentiment via voice and facial cues.
- [ ] **Reinforcement Learning**: Tuning coaching feedback based on trader performance improvement.
- [ ] **Advanced Retrieval**: Implementing vector-based RAG for more nuanced memory recall.
- [ ] **Personalization**: Hyper-personalized risk-management thresholds based on individual equity curves.

---

## 👨‍💻 Author

<div align="center">

### **Piyush Ramteke**
*AI Researcher & Software Engineer*

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Piyu242005)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/piyu24/)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://piyu242005.github.io/Piyush-Ramteke/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:piyushramteke24@gmail.com)

</div>

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer&text=Innovating%20Behavioral%20Finance&fontSize=20" width="100%" />
  <p>Built with ❤️ for the Open Source AI Community</p>
</div>
