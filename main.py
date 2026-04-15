
#uvicorn main:app --reload thus will start the FastAPI application with hot-reloading enabled, allowing you to see changes in real-time without restarting the server.

# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager  # ← NEW: For lifespan management
from sqlalchemy import create_engine, text
from api.v1.domain import router as domain_router
from core.config import DOMAIN_DB_MAPPING, settings
import logging
from datetime import datetime
from core.database import db_manager
from models.base import Base  # ← Import Base for table creation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n🚀 Resetting tables...")

    try:
        engine = db_manager.engines["master"]

        # ❌ Drop old tables
        Base.metadata.drop_all(bind=engine)

        # ✅ Create new tables
        Base.metadata.create_all(bind=engine)

        print("✅ Tables recreated successfully")
    except Exception as e:
        print("❌ Error:", e)
    yield
    print("🛑 Shutting down...")

# =============================================================================
# 🎯 FASTAPI APP INITIALIZATION
# =============================================================================
app = FastAPI(
    title="BRE_ANALYSOR - Multi-Domain API",
    description="Multi-tenant API for speedoloan, rupylalao, and 5mint domains",
    version="1.0.0",
    lifespan=lifespan  # ← REGISTER LIFESPAN HANDLER (Critical!)
)

# =============================================================================
# 🔐 CORS MIDDLEWARE
# =============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# 📦 INCLUDE ROUTERS
# =============================================================================
app.include_router(domain_router, prefix="/api",)


# =============================================================================
# 🏠 ROOT ENDPOINT
# =============================================================================
# @app.get("/")
# async def root():
#     return {
#         "message": "BRE_ANALYSOR API",
#         "version": "1.0.0",
#         "domains": ["speedoloan", "rupylalao", "5mint"],
#         "docs": "/docs",
#         "health_check": "/api/health/db"
#     }


# =============================================================================
# 🩺 HEALTH CHECK ENDPOINTS (NEW - Optional but Recommended)
# =============================================================================
@app.get("/api/health")
async def health_check():
    """Basic API health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "BRE_ANALYSOR"
    }


@app.get("/api/health/db")
async def check_domain_databases():
    """
    Check connectivity to all domain databases on-demand.
    Useful for monitoring, load balancers, or manual verification.
    """
    results = {}
    for domain, db_url in DOMAIN_DB_MAPPING.items():
        try:
            engine = create_engine(
                db_url, 
                pool_pre_ping=True, 
                connect_args={"connect_timeout": 3}
            )
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            results[domain] = {
                "status": "connected",
                "message": "OK"
            }
        except Exception as e:
            results[domain] = {
                "status": "failed",
                "message": str(e)[:150]  # Truncate long errors
            }
        finally:
            engine.dispose()
    all_connected = all(r["status"] == "connected" for r in results.values())
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "overall_status": "healthy" if all_connected else "degraded",
        "domains": results
    }

# =============================================================================
# 📝 REQUEST LOGGING MIDDLEWARE (Fixed - Actually Logs!)
# =============================================================================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests with method, path, and status"""
    start_time = datetime.utcnow()
    logger.info(f"→ {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        process_time = (datetime.utcnow() - start_time).total_seconds()
        logger.info(f"← {request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)")
        return response
    except Exception as e:
        logger.error(f"✗ {request.method} {request.url.path} - Error: {e}")
        raise

# =============================================================================
# 🏃 APPLICATION ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    import uvicorn
    
    print("\n💡 Starting with: python main.py")
    print("   For hot-reload dev: uvicorn main:app --reload\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False  # Set True only if running directly with reload support
    )