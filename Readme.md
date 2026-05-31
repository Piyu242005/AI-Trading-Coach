<!-- 
AI TRADING COACH - PROFESSIONAL README
Designed for Recruiters, Researchers, and AI Maintainers
-->

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

## 📈 Portfolio Metrics
<div align="center">
  <img src="https://img.shields.io/badge/Trades_Analyzed-25+-10B981?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI_Confidence-95%25-F59E0B?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Discipline_Score-79-3B82F6?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Profit_Factor-3.07-8B5CF6?style=for-the-badge" />
</div>

<br />

## 🎯 Overview

The **AI Trading Coach** is a sophisticated full-stack SaaS application designed to mitigate emotional and cognitive biases in financial decision-making. By combining **Retrieval-Augmented Generation (RAG)** with a **Persistent Memory System**, the platform tracks a trader's activity across sessions to detect behavioral "pathologies" and provide real-time, evidence-based coaching.

### 🔬 Explainable AI (XAI)
Unlike "black-box" AI advisors, this project prioritizes **Explainable AI**. Every coaching insight is backed by a verifiable audit trail, mapping AI-generated advice directly to historical trade data, ensuring zero-hallucination and high reliability.

---

## ✨ Key Features

| Feature | Category | Description |
| :--- | :--- | :--- |
| 💬 **ChatGPT-Style Coaching** | `UX` | Real-time, streaming markdown UI for interactive behavioral feedback. |
| 🧠 **Behavioral Profiling** | `AI Engine` | Detects pathologies (FOMO, Revenge Trading, Tilt) with severity & confidence metrics. |
| 📊 **Advanced Analytics** | `Frontend` | Glassmorphic dashboard with Recharts-powered Equity Curves and Risk Distribution. |
| 📚 **RAG-Powered Memory** | `Architecture` | Persistent MongoDB-backed memory retaining session context and user-specific patterns. |
| 🛡️ **Anti-Hallucination Audit** | `Reliability` | A rigorous verification layer cross-referencing AI outputs with ground-truth records. |

---

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

---

## 📂 Project Structure

```text
AI-Trading-Coach/
├── frontend/            # React + Vite Application
│   ├── src/pages/       # Dashboard, Coaching, Profiling, Journal
│   └── src/services/    # Axios API client
├── app/                 # FastAPI application (Routes, Models, Services)
│   ├── routes/          # API endpoints (Coaching, Memory, Profiling, Audit)
│   ├── services/        # Core business logic & heuristic engines
│   ├── main.py          # Entry point & lifecycle management
│   └── auth.py          # JWT & Identity Management
├── .github/workflows/   # CI/CD Pipelines (Backend & Frontend tests)
├── data/                # Ground-truth datasets & behavioral labels
└── tests/               # E2E test suite (Pytest)
```

---

## 🚀 Setup Instructions

### 🐳 Method 1: Docker (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/Piyu242005/AI-Trading-Coach.git
cd AI-Trading-Coach

# 2. Spin up containers
docker-compose up --build -d
```

### 🐍 Method 2: Local Development
```bash
# 1. Install Backend dependencies
pip install -r requirements.txt

# 2. Run the FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 3. In a new terminal, install Frontend dependencies
cd frontend
npm install

# 4. Run the Vite React server
npm run dev
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/auth/token` | `POST` | Exchange credentials for a JWT Access Token. |
| `/api/discipline-score/{userId}` | `GET` | Fetches the AI-calculated behavioral discipline score. |
| `/api/coaching/{userId}/stream` | `POST` | Real-time ChatGPT-style coaching feedback via Server-Sent Events. |
| `/api/profiling/{userId}` | `GET` | Fetch behavioral profiles (severity, confidence, impacts). |
| `/api/trades` | `GET` | Return paginated historical trades with emotional states. |

---

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
