Here is a **clear, short roadmap** to complete **Track 2: System of AI Engine (AI/ML)** efficiently:

---

# 🧠 Track 2 Roadmap (Step-by-Step)

## 🎯 Goal

Build an **AI trading coach** that:

* Understands trader behavior
* Stores memory (no hallucination)
* Gives real-time coaching
* Produces evaluation metrics

---

## 🏗️ Phase 1: Setup (2–3 hours)

* Tech:

  * Python (FastAPI)
  * JSON dataset load
* Load `nevup_seed_dataset.json`
* Create basic project structure

👉 Output: API running + data loaded

---

## 📊 Phase 2: Behavioral Profiling (Core)

* Analyze each trader:

  * Detect patterns (FOMO, overtrading, etc.)
* Use **rule-based logic first**

Example:

* Many trades in short time → Overtrading
* Loss + immediate trade → Revenge

👉 Output: Structured profile with **evidence (tradeId, sessionId)**

---

## 🧠 Phase 3: Memory System (Very Important)

Build 3 APIs:

1. `PUT /memory/{userId}/sessions/{sessionId}`

   * Store summary + metrics

2. `GET /memory/{userId}/context`

   * Retrieve relevant past sessions

3. `GET /memory/{userId}/sessions/{sessionId}`

   * Return exact stored data

👉 Use:

* PostgreSQL / MongoDB (persistent storage)

👉 Key:

* **No fake memory (must match real data)**

---

## ⚡ Phase 4: Coaching Engine

* Input: stream of trades

* Detect signals:

  * Overtrading
  * Tilt
  * Revenge trading

* Generate message:

Example:

```
"You placed 3 trades after a loss. This indicates revenge trading. Pause and reassess."
```

👉 Keep logic:

* Simple + explainable

---

## 🔄 Phase 5: Streaming Response

* Use:

  * SSE (Server-Sent Events)

* Send message **token-by-token**

👉 Improves UX + meets requirement

---

## 🔍 Phase 6: Anti-Hallucination Audit

* API: `POST /audit`
* Check:

  * All sessionIds in response exist

Output:

```
sessionId → found / not found
```

👉 Critical for scoring

---

## 📈 Phase 7: Evaluation Harness

* Use 10 traders dataset
* Predict pathology

Calculate:

* Precision
* Recall
* F1 Score

👉 Output: JSON/HTML report

---

## 🔐 Phase 8: Authentication

* JWT-based
* Ensure:

  * userId == token.sub
* Else → 403

---

## 🐳 Phase 9: Docker Setup

* Create `docker-compose.yml`
* One command run:

```
docker-compose up
```

---

## 🧪 Phase 10: Testing

* Test all APIs
* Check:

  * Memory persistence
  * No hallucination
  * Response < 3 sec

---

# 🧾 Final Architecture

```
Dataset → Profiling → Memory DB
                ↓
        Coaching Engine → Streaming API
                ↓
         Evaluation + Audit
```

---

## 🎯 Winning Tips

* Focus on **accuracy + explainability**
* Avoid complex ML → start with **rules**
* Always **cite sessionId + tradeId**
* Make system **deterministic (same input → same output)**

---

## ⏱️ Suggested Timeline (72 hrs)

* Day 1 → Setup + Profiling
* Day 2 → Memory + Coaching
* Day 3 → Evaluation + Docker + Testing

