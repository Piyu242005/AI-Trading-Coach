from fastapi import FastAPI, HTTPException
from app.routes import auth, coaching, evaluation, memory, profiling, traders, audit
from app.mongodb import client

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Piyu API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8501", "http://127.0.0.1:5173", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {
        "project": "AI Trading Coach",
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