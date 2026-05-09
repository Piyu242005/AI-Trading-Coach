# 🎯 Track 2 Case Study: System of AI Engine Requirements

> **Core Objective:** Build a **smart, memory-based AI system (not just a chatbot)** that understands trader behavior, retains past session memory, and provides accurate, verifiable, and explainable coaching.

---

## 🏗️ 1. Core Architecture Requirements

### 🧠 Behavioral Understanding
The system must actively read and analyze trader data to identify specific behavioral pathologies:
- 📉 **FOMO (Fear Of Missing Out)**
- 🔁 **Overtrading**
- 😡 **Revenge Trading**

> **🚨 CRITICAL RULE:** Every claim made by the AI MUST include verifiable proof, specifically citing the exact `sessionId` and `tradeId`.

### 💾 Persistent Memory System
This is the **primary focus of Track 2**. The system must:
- Store context from past trading sessions.
- Accurately retrieve this context when relevant.
- **Maintain persistence** across system restarts (Memory must not be forgotten).

---

## ⚙️ 2. Execution & Delivery

### 🗣️ Streaming Coaching Engine
The AI must react to trades as they happen, delivering context-aware advice based on real data.
- **Input:** Live trading events.
- **Output:** Explainable advice. *(e.g., "You are trading right after multiple losses → possible revenge trading detected.")*

### ⚡ Real-Time Response
- Coaching must be streamed without delay.
- Use **Server-Sent Events (SSE)** or **WebSockets** for delivery.

---

## 🛡️ 3. Verification & Validation

### 🚫 No Hallucination Audit (Critical)
The AI should **NEVER** generate fake references or hallucinate data.
- If it references "Session 123", Session 123 must verifiably exist in the database.
- An **Audit System** must be built to mathematically verify these claims.

### 📊 Evaluation System
The model's effectiveness must be quantified by running it against a labeled dataset. Outputs must include:
- **Precision**
- **Recall**
- **F1 Score**

*(This provides empirical evidence that the model functions correctly).*

---

## ⚠️ What They DON’T Want (Anti-Patterns)
- ❌ **Fancy Chatbots:** LLM wrappers without underlying logic or deterministic validation.
- ❌ **Random LLM Answers:** Unconstrained text generation.
- ❌ **Amnesia:** Systems with no memory or evidence backing.
- ❌ **Hardcoded/Fake Results:** Faked outputs to pass evaluations.

---

## 💡 Summary & Mindset

### The One-Liner Summary
> Build a **smart, memory-based AI coach that gives proven, explainable advice from real data.**

### 🧠 The Architectural Mindset
Shift your perspective from simple LLM integration to a comprehensive pipeline:

**❌ INCORRECT:** *"AI gives advice"*  
**✅ CORRECT:** *"System analyzes → proves → remembers → explains → responds"*

---

## ✅ Final Delivery Pipeline
Your final submission should clearly demonstrate:
**Data Ingestion ➔ Logic Processing ➔ Memory Retention ➔ Coaching Delivery ➔ Validation & Audit**