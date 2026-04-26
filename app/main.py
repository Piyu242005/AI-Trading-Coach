from fastapi import FastAPI, HTTPException
from app.routes import auth, coaching, evaluation, memory, profiling, traders, audit
from app.mongodb import client

app = FastAPI(title="NevUp API")

@app.get("/")
def read_root():
    return {
        "message": (
            "Welcome to the NevUp API! Access trades at /api/trades, profiling at "
            "/api/profiling/{userId}, memory at /api/memory/{userId}, coaching at "
            "/api/coaching/{userId}, audit at /audit, and evaluation at /evaluation/report"
        ),
        "status": "API running + data loaded successfully.",
    }

@app.get("/health")
def health():
    try:
        client.admin.command('ping')
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

app.include_router(traders.router, prefix="/api")
app.include_router(profiling.router, prefix="/api/profiling")
app.include_router(memory.router, prefix="/api/memory")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(coaching.router, prefix="/api/coaching")
app.include_router(audit.router)
app.include_router(evaluation.router)