Here is a **simple, clear explanation** of what **System of AI Engine (Track 2)** actually wants:

---

# 🎯 Core Idea

They want you to build an **AI system (not just a chatbot)** that:
👉 Understands trader behavior
👉 Remembers past sessions
👉 Gives **accurate, explainable coaching**

---

# 🧠 What You MUST Build

## 1. Behavioral Understanding

* Read trader data
* Identify problems like:

  * FOMO
  * Overtrading
  * Revenge trading

👉 Important:
Every claim must include **proof (sessionId + tradeId)**

---

## 2. Memory System (Very Important)

* Store past sessions
* Retrieve when needed
* Must **not forget after restart**

👉 This is the main focus of this track

---

## 3. Coaching Engine

* Input: trades happening
* Output: advice

Example:
“You are trading right after losses → possible revenge trading”

👉 Must be:

* Context-aware
* Based on real data

---

## 4. No Hallucination (Critical)

* AI should NOT make fake references
* If it says “Session 123” → it must exist

👉 You must build an **audit system** to verify this

---

## 5. Real-Time Response

* Coaching should stream (not delayed)
* Use SSE / WebSocket

---

## 6. Evaluation System

* Run your model on dataset
* Output:

  * Precision
  * Recall
  * F1 Score

👉 Shows your model works correctly

---

# ⚠️ What They DON’T Want

* ❌ Fancy chatbot without logic
* ❌ Random LLM answers
* ❌ No evidence / no memory
* ❌ Fake or hardcoded results

---

# 🧾 In One Line

👉 Build a **smart, memory-based AI coach that gives proven, explainable advice from real data**

---

# 🧠 Think Like This

Not:

> “AI gives advice”

But:

> “System analyzes → proves → remembers → explains → responds”

---

## ✅ Final Understanding

You are building:

* **Data → Logic → Memory → Coaching → Validation**

---