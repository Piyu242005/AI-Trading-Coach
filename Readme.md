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

## Tech Stack
Frontend:
- Streamlit
- Plotly

Backend:
- FastAPI
- Python

AI and ML:
- OpenAI or Ollama (pluggable)
- Scikit-Learn
- Pandas
- NumPy

Database:
- PostgreSQL or SQLite (configurable)

DevOps:
- Docker
- GitHub Actions

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
