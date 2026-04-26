# AI Trading Coach: Engineering Implementation Roadmap

This document outlines the structured execution plan and core architectural principles for developing the AI Trading Coach (Track 2: System of AI Engine).

---

## 1. Project Objective
Develop a real-time AI trading coach that accurately detects behavioral pathologies, provides context-aware feedback with zero hallucination, and evaluates its own predictive accuracy against ground-truth datasets.

---

## 2. Implementation Phases

### Phase 1: Foundation & Data Ingestion
- **Objective:** Establish the API framework and load seed data.
- **Execution:** Initialize the FastAPI application, configure the MongoDB connection via motor/pymongo, and implement the JSON dataset loader for `nevup_seed_dataset.json`.

### Phase 2: Behavioral Profiling Logic
- **Objective:** Detect behavioral anomalies (e.g., Overtrading, Revenge Trading, FOMO).
- **Execution:** Implement deterministic, rule-based heuristics to analyze sequential user trading sessions. Ensure every detected pathology is strictly tied to verifiable evidence (e.g., specific `sessionId` and `tradeId`).

### Phase 3: Persistent Memory Subsystem
- **Objective:** Retain long-term user context across API lifecycles.
- **Execution:** Build robust REST endpoints to store session summaries and retrieve historical context. Enforce strict database validation to prevent memory hallucinations or data corruption.

### Phase 4: Coaching Engine & Streaming
- **Objective:** Deliver low-latency, actionable trading insights.
- **Execution:** Connect the deterministic profiling engine to a Server-Sent Events (SSE) stream. Output coaching tokens sequentially to mimic conversational AI dynamics, ensuring all responses explicitly cite the user's historical data.

### Phase 5: Audit & Evaluation Harness
- **Objective:** Validate system accuracy and enforce data integrity.
- **Execution:** 
  - Develop an `/audit` API endpoint to strictly verify that all referenced session/trade IDs actually exist in the database.
  - Implement an automated evaluation script (`evaluate.py`) to calculate Precision, Recall, and F1 Scores across the 10-trader ground-truth dataset.

### Phase 6: Security & Deployment
- **Objective:** Secure the API endpoints and ensure a reproducible deployment environment.
- **Execution:** Implement PyJWT-based authentication to bind access tokens to specific `userId`s. Containerize the application components (FastAPI + MongoDB) using Docker and Docker Compose for a seamless one-command startup.

---

## 3. Core Architectural Principles

- **Accuracy over Complexity:** Prioritize deterministic rule-based logic over black-box machine learning to guarantee 100% explainability.
- **Strict Anti-Hallucination:** The system must never fabricate data. All coaching advice must cite real, verifiable database records.
- **Stateless API / Stateful Storage:** Maintain web server statelessness to allow for horizontal scaling by delegating all memory persistence to MongoDB.
- **Reproducibility:** The system's output must remain entirely deterministic—identical inputs must consistently produce identical coaching outputs and evaluation metrics.
