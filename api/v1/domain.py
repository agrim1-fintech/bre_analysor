from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from typing import Optional
from core.database import get_db_session
from core.security import DomainSecurity
from schemas.domain import DomainCreate, DomainResponse
from models.domain import Domain
import logging

# logger = logging.getLogger(__name__)
router = APIRouter()

# async def get_current_domain(
#     x_domain_key: str = Header(..., description="Domain API Key"),
#     request: Request = None
# ):
#     """Dependency to validate domain and get database session"""
#     # Get master database session (for domain validation)
#     master_db = next(get_db_session("speedoloan"))  # Use any domain's session for master
    
#     try:
#         # Validate domain key
#         domain = await DomainSecurity.validate_domain_key(master_db, x_domain_key)
#         if not domain:
#             raise HTTPException(
#                 status_code=401,
#                 detail="Invalid or inactive domain key"
#             )
        
#         # Get domain-specific database session
#         domain_db = next(get_db_session(domain.domain_name))
        
#         return {
#             "domain": domain,
#             "db": domain_db
#         }
#     finally:
#         master_db.close()

# @router.get("/health")
# async def health_check(domain_info: dict = Depends(get_current_domain)):
#     """Health check endpoint for domain"""
#     return {
#         "status": "healthy",
#         "domain": domain_info["domain"].domain_name,
#         "database": domain_info["domain"].database_name
#     }

# @router.get("/info")
# async def get_domain_info(domain_info: dict = Depends(get_current_domain)):
#     """Get domain information"""
#     domain = domain_info["domain"]
#     return {
#         "domain_name": domain.domain_name,
#         "database_name": domain.database_name,
#         "is_active": domain.is_active,
#         "created_at": domain.created_at
#     }

# # Example domain-specific endpoint
# @router.get("/data")
# async def get_domain_data(
#     domain_info: dict = Depends(get_current_domain)
# ):
#     """Example endpoint that uses domain-specific database"""
#     db = domain_info["db"]
#     domain = domain_info["domain"]
    
#     # Query domain-specific data
#     # Example: data = db.query(YourModel).all()
    
#     return {
#         "message": f"Data from {domain.domain_name} database",
#         "domain": domain.domain_name
#     }

@router.post("/domain", response_model=DomainResponse)
def create_domain(payload: DomainCreate):
    db = next(get_db_session("master"))
    try:
        existing = db.query(Domain).filter(
            Domain.domain_name == payload.domain_name
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Domain already exists")
        # ✅ Create new domain
        new_domain = Domain(**payload.dict())
        db.add(new_domain)
        db.commit()
        db.refresh(new_domain)

        return new_domain
    finally:
        db.remove()