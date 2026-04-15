

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.v1.domain import router as domain_router   # ← Correct import
from core.config import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="BRE_ANALYSOR - Multi-Domain API",
    description="Multi-tenant API for speedoloan, rupylalao, and 5mint domains",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - FIXED
app.include_router(domain_router, prefix="/api", tags=["domains"])   # ← No trailing slash + correct router

@app.get("/")
async def root():
    return {
        "message": "BRE_ANALYSOR API",
        "domains": ["speedoloan", "rupylalao", "5mint"],
        "docs": "/docs"
    }

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)