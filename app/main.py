from fastapi import FastAPI
from app.routes import traders, profiling, memory

app = FastAPI(title="NevUp API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the NevUp API! Access trades at /api/trades, profiling at /api/profiling/{userId}, and memory at /api/memory",
    "status": "API running + data loaded successfully."}

app.include_router(traders.router, prefix="/api")
app.include_router(profiling.router, prefix="/api/profiling")
app.include_router(memory.router, prefix="/api/memory")