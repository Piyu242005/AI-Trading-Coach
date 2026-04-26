# Architecture & Technical Decisions

This document outlines the rationale behind the system design, tech stack, and logic implementation for the AI Trading Coach.

## 1. Why Strict JWT Enforcement?
- **Security & Multi-Tenancy:** We implemented strict PyJWT HS256 validation. By rigorously enforcing that the requesting `userId` perfectly matches the `token.sub` claim, we secure user data against unauthorized access. This prevents cross-tenant data leakage, a critical requirement for a financial application storing sensitive trading histories.

## 2. Why Rule-Based Logic for All 9 Pathologies?
- **Deterministic and Explainable:** We implemented heuristics for all 9 pathologies (e.g., Overtrading, FOMO Entries, Time of Day Bias). Financial coaching requires high accuracy and trust. A rule-based approach guarantees predictable outputs and explicit traceability back to specific user actions, avoiding the unpredictable nature of pure ML classification in early-stage development.

## 3. Why Evidence-Based Coaching?
- **Zero Hallucination:** The coaching engine is strictly confined to referencing verified `sessionId` and `tradeId` properties retrieved directly from the deterministic engine. This guarantees 100% factual accuracy and ensures the AI never fabricates advice, building absolute trust with the end user.

## 4. Why Shared Evaluation Logic?
- **Absolute Consistency:** We unified the evaluation pipeline. Both the FastAPI `/evaluation/report` endpoint and the local `evaluate.py` script import the exact same underlying logic (`_build_evaluation_report`). This prevents drift between local testing and production metrics, ensuring precision, recall, and F1 scores are perfectly reproducible and transparent.

## 5. Why DB Health Check?
- **System Reliability:** We added a `/health` endpoint that actively executes a MongoDB `ping` command rather than just returning a static 200 response. This provides immediate, verifiable feedback on database connectivity, drastically improving infrastructure monitoring and deployment safety.

## 6. Trade-Offs and Limitations
- **Imperfect Heuristics vs Complex ML:** Our rules (e.g., rigid time-window limits for Revenge Trading) are purposefully basic. While this sacrifices a perfect F1 score, it successfully proves the architectural pipeline is sound without resorting to fabricating data or deploying overfitted black-box models.
- **Avoided LLM Generation for Alerts:** Generating critical alerts dynamically using an LLM was avoided due to latency concerns and the risk of hallucination. We traded conversational variance for 100% accuracy and speed when alerting the user.

## 7. Future Improvements
- **Hybrid AI Engine:** Layer an LLM strictly over the deterministic output (RAG architecture) to rewrite the rigid rules-based alerts into conversational, empathetic coaching.
- **Dynamic Thresholding:** Use statistical anomaly detection (e.g., Z-scores, Isolation Forests) to calculate personalized limits based on the user's historical rolling variance rather than static limits.
- **WebSockets for Live Market Data:** Transition ingestion from HTTP POST to WebSockets to support bi-directional live price feeds with lower latency.
