<div align="center">
  
# AI Trading Coach

**AI-Powered Trading Intelligence, Behavioral Analytics & Portfolio Optimization Platform**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Machine_Learning-orange)](https://xgboost.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/SHAP-Explainable_AI-brightgreen)](https://shap.readthedocs.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Data_Viz-purple)](https://plotly.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)

</div>

## 📖 Overview

An AI-powered trading intelligence platform that helps traders improve decision-making through predictive analytics, explainable machine learning, behavioral insights, portfolio analytics, and conversational AI coaching.

---

## ✨ Core Features

### 📊 Trading Insights Coach
* Record-based summaries and historical metrics
* Natural-language keyword routing to deterministic analytics
* Clear disclosure that this version does not call an external LLM

### 📈 Trade Prediction Engine
* XGBoost-powered prediction model
* Trade success probability scoring
* Risk estimation
* Confidence metrics

### 🔍 Model Explainability Sandbox
* SHAP feature-contribution visualization when supported by the installed model/runtime
* Explicit warning that model artifacts use synthetic training data
* Graceful fallback when SHAP output is unavailable

### 🧠 Behavioral Analytics Readiness
* Trade history normalization and outcome counts
* Recorded strategy/confidence fields surfaced when present
* Behavioral scores are not generated when supporting data is missing

### 📊 Trade Performance Analytics
* Net P&L, historical win rate, profit factor, and drawdown
* Trade count and P&L by asset
* Clear distinction between trade-level statistics and a complete portfolio valuation

### 📉 Trade-Price Analysis
* Recorded entry-price charts and rolling averages
* Descriptive price variation where enough records exist
* No fabricated price history or claims of live market data

### 📓 Trading Journal
* Trade Logging
* Strategy Evaluation
* Performance Review
* Learning Notes

### 💡 AI Insights Engine
* Trade Pattern Detection
* Winning Strategy Discovery
* Loss Pattern Analysis
* Personalized Improvement Recommendations

---

## 🖥️ Interface & Demo Notes

The Streamlit interface includes a dashboard, trade-history charts, a record-based insights coach, a prediction sandbox, a trading journal, and portfolio analytics.

- Guest mode uses illustrative sample trades; it does not connect to live market prices.
- Market charts only use recorded trade prices. Missing data is shown as unavailable rather than generated.
- Prediction artifacts are trained on synthetic data for demonstration and must not be interpreted as real-market probabilities.
- The current backend token endpoint accepts a user ID without password verification. Do not use sensitive account or portfolio data until proper authentication and authorization are implemented.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[User] -->|Interacts| B(Streamlit Frontend)
    B -->|API Calls| C(FastAPI Backend)
    
    subgraph Core AI Services
    C --> D{AI Coach Layer}
    C --> E[Trade Prediction Engine XGBoost]
    E --> F[Explainability Layer SHAP]
    C --> G[Portfolio Intelligence Engine]
    end
    
    C --> H[(Database PostgreSQL/SQLite)]
    D -.-> H
    G -.-> H
```

---

## 🧠 Machine Learning Pipeline

Data Collection → Feature Engineering → Model Training → Prediction → Explainability → Portfolio Intelligence

1. **Data collection:** The current demo accepts sample trade records and API-provided records.
2. **Feature engineering:** A deterministic synthetic dataset is generated for the model demonstration.
3. **Model training:** An `XGBClassifier` is trained with a holdout split; preprocessing is fitted on training data only.
4. **Prediction:** The app displays a model score for user-supplied synthetic-scale features.
5. **Explainability:** SHAP contributions are rendered when compatible with the model and runtime.
6. **Evaluation boundary:** Synthetic-data metrics are diagnostic only and are not evidence of real-world trading performance.

---

## 🛠️ Tech Stack

**Frontend:**
* Streamlit
* Plotly

**Backend:**
* FastAPI
* Python

**Machine Learning:**
* XGBoost
* Scikit-Learn
* SHAP
* Pandas
* NumPy

**Database:**
* PostgreSQL / SQLite

**DevOps:**
* Docker
* GitHub Actions

---

## 📐 Metrics & Evaluation

Dashboard metrics are calculated from the trade records currently loaded into the app: trade count, historical win rate, net P&L, profit factor, and peak-to-trough drawdown from cumulative trade P&L.

The demo model training script reports holdout accuracy, precision, recall, F1, and ROC AUC on a synthetic dataset. These are **synthetic-data diagnostics**, not evidence of trading performance. No real-world accuracy or latency claim is made.

---

## 📂 Project Structure

```text
AI-Trading-Coach/
├── .github/workflows/      # CI/CD Pipelines
├── app/                    # FastAPI Backend
│   ├── routes/             # API Endpoints (Auth, Coaching, Discipline)
│   ├── services/           # Business Logic & NLP Handlers
│   ├── main.py             # Server Entrypoint
│   └── database.py         # DB Connectors
├── data/                   # Seed Datasets
├── frontend-streamlit/     # Streamlit Frontend App
│   ├── models/             # Serialized ML Models (XGBoost, Scaler)
│   ├── training/           # ML Training & Feature Engineering Scripts
│   ├── app.py              # UI Entrypoint
│   └── requirements.txt    
├── tests/                  # PyTest Suite
├── docker-compose.yml      # Container Orchestration
└── Readme.md
```

---

## 🔐 Secure Backend Configuration

The API intentionally has **no default credentials**. Configure a strong JWT signing secret and a password-hash map before enabling login.

1. Generate a password hash locally (password input is hidden):

   ```bash
   python scripts/hash_password.py
   ```

2. Generate a strong JWT secret:

   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(48))"
   ```

3. Configure these environment variables in your API host (or export them before Docker Compose):

   - `JWT_SECRET`: the generated secret (at least 32 characters).
   - `AI_TRADING_COACH_USERS_JSON`: JSON mapping user IDs to the hash output, e.g. `{"Piyu24":"<salt_hex>:<pbkdf2_hash_hex>"}`.

   Do not commit actual secrets, password hashes, or `.env` files. Without valid configuration, login fails closed and Guest demo remains available.

## 💻 Installation Guide

### 1. Clone the repository
```bash
git clone https://github.com/Piyu242005/AI-Trading-Coach.git
cd AI-Trading-Coach
```

### 2. Frontend Setup (Streamlit & ML)
```bash
cd frontend-streamlit
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Generate the ML Models
cd training
python train_model.py
cd ..

# Run the UI
streamlit run app.py
```

### 3. Backend Setup (FastAPI - Optional for Local Dev)

Configure the secure backend environment variables above, then run:

```bash
docker-compose up --build
```

---

## 🛣️ Future Roadmap

* **RAG-powered Trading Knowledge Base**: Ingest Investopedia and textbook PDFs for semantic QA.
* **Multi-Agent Trading Assistant**: Specialized agents for risk, fundamental analysis, and technicals.
* **Market Sentiment Analysis**: Twitter/X and News sentiment NLP pipelines.
* **Reinforcement Learning Strategies**: PPO-based automated trading bots.
* **Real-Time Data Feeds**: WebSockets integration for live tick data.
* **Advanced Risk Optimization**: Markowitz Efficient Frontier generation.

---

## 🌟 Project Strengths & Current Boundaries

This repository demonstrates a Streamlit + FastAPI architecture, data visualization, an XGBoost training workflow, model serialization, and test automation.

**Important boundaries:** the bundled model is trained on synthetic data; the Streamlit coach uses deterministic record-based rules rather than an external LLM; the current API token endpoint does not verify a password; and journal entries are not persisted. These limitations must be addressed before describing the app as production-ready.

## 💼 Resume Highlights

Use wording that accurately reflects the current prototype:

- Built a Streamlit trading analytics dashboard with Plotly visualizations for historical win rate, net P&L, profit factor, and drawdown.
- Implemented a reproducible XGBoost demonstration pipeline with a train/holdout split and preprocessing fitted only on training data.
- Added SHAP-based feature contribution visualizations with graceful fallback handling.
- Integrated a Streamlit frontend with a FastAPI backend and added automated tests for trade analytics.

Avoid claiming real-world prediction accuracy, sub-500ms inference, persistent journal storage, secure production authentication, or live market-data ingestion until those capabilities are implemented and verified.

