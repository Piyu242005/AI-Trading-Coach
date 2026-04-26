# Architecture & Technical Decisions

This document outlines the rationale behind the system design, tech stack, and logic implementation for the AI Trading Coach.

## 1. Why Rule-Based Heuristics (Over Pure ML)?
- **Deterministic and Explainable:** Financial coaching requires high accuracy and trust. A rule-based approach for detecting pathologies (e.g., Overtrading, Revenge Trading) guarantees predictable outputs and explicit traceability back to specific user actions.
- **Data Constraints:** Synthesized or limited datasets make training robust deep learning models challenging without risking overfitting. Rules act as a solid, verifiable baseline before scaling to complex ML models.

## 2. Why MongoDB?
- **Flexible Schema:** Trade data and user profiles are highly hierarchical and schema-less by nature. Document storage perfectly matches the nested structure of our JSON inputs.
- **Fast Iteration:** Allows rapid updates to the memory schema and nested session arrays without complex database migrations during a tight hackathon timeline.

## 3. Memory Design & Persistence
- **Structure:** Memory is strictly partitioned by `userId` and `sessionId`. It stores aggregate performance statistics and rolling windows of recent raw trades.
- **Persistence Strategy:** Binds state securely across API restarts, allowing the coaching engine to maintain deep longitudinal context of the user rather than just reacting to isolated, single trades.

## 4. Why Server-Sent Events (SSE) for Streaming?
- **Unidirectional Flow:** The server pushes coaching tokens in real-time, matching the UX of modern AI chat interfaces (like ChatGPT).
- **Simpler than WebSockets:** SSE operates over standard HTTP, avoiding connection state overhead and complex proxy configurations while delivering identical text-streaming performance for the end user.

## 5. Preventing Hallucination
- **Hard Grounding:** The coaching logic is strictly confined to referencing verified `sessionId` and `tradeId` properties retrieved directly from the deterministic engine.
- **Audit Verification:** We utilize a verification mechanism that cross-checks generated insights against the persistent MongoDB memory before dispatching advice to the client, guaranteeing 100% factual accuracy. 

## 6. Trade-Offs
- **Avoided LLM Generation for Alerts:** Generating critical alerts dynamically using an LLM was avoided due to latency concerns and the risk of hallucination. We traded conversational variance for 100% accuracy and speed when alerting the user to dangerous behaviors.
- **Batch Processing vs Broker Streaming:** We simulated a stream rather than deploying a heavy messaging broker (like Kafka), prioritizing ease-of-deployment and a lower resource footprint.

## 7. Scalability Considerations
- **Stateless API Instances:** FastAPI instances run statelessly. Memory state is fully delegated to MongoDB, allowing horizontal scaling of the web instances.
- **Async Operations:** I/O bound tasks (like SSE streaming and database queries) leverage Python's `asyncio` to handle concurrent user connections efficiently without blocking the main thread.

## 8. Limitations of Current System
- **Rigid Rulesets:** The heuristic thresholds are currently static (e.g., fixed volume counts for overtrading) and do not adapt dynamically to the varying volatility profiles of different assets.
- **No Push-to-Client Signals:** The client must actively listen to the SSE stream. It currently lacks Webhook integration for background alerts if the user closes the dashboard.

## 9. Future Improvements
- **Hybrid AI Engine:** Layer an LLM over the deterministic output to rewrite the rigid rules-based alerts into conversational, empathetic coaching.
- **Dynamic Thresholding:** Use statistical anomaly detection (e.g., Z-scores, Isolation Forests) to calculate personalized limits based on the user's historical rolling variance.
- **WebSockets for Live Market Data:** Transition ingestion to WebSockets for bi-directional live price feeds.
