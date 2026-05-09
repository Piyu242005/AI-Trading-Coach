from fastapi import FastAPI, HTTPException
from app.routes import auth, coaching, evaluation, memory, profiling, traders, audit
from app.mongodb import client

app = FastAPI(title="NevUp API")

@app.get("/")
def read_root():
    return {
        "project": "NevUp AI Trading Coach",
        "author": "Piyush Ramteke",
        "status": "🟢 API Online • Data Loaded Successfully",
        "description": "Explainable Behavioral AI System for Reliable Financial Decision Support",
        "core_features": [
            "Behavioral Pathology Detection",
            "Retrieval-Augmented Coaching",
            "Persistent Memory Engine",
            "Anti-Hallucination Audit",
            "Real-Time Streaming Feedback"
        ],
        "available_endpoints": {
            "trades": "/api/trades",
            "profiling": "/api/profiling/{userId}",
            "memory": "/api/memory/{userId}",
            "coaching": "/api/coaching/{userId}",
            "audit": "/audit",
            "evaluation": "/evaluation/report"
        },
        "tech_stack": [
            "FastAPI",
            "MongoDB",
            "Python",
            "LangChain",
            "Docker"
        ],
        "live_demo": "https://ai-trading-coach-2vao.onrender.com",
        "github": "https://github.com/Piyu242005/AI-Trading-Coach"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(traders.router, prefix="/api")
app.include_router(profiling.router, prefix="/api/profiling")
app.include_router(memory.router, prefix="/api/memory")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(coaching.router, prefix="/api/coaching")
app.include_router(audit.router)
app.include_router(evaluation.router)