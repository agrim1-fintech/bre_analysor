from sqlalchemy.orm import Session
from models.domain import Domain
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DomainSecurity:
    @staticmethod
    async def validate_domain_key(db: Session, domain_key: str) -> Optional[Domain]:
        """Validate domain key and return domain info"""
        try:
            domain = db.query(Domain).filter(
                Domain.domain_key == domain_key,
                Domain.is_active == True
            ).first()
            
            if domain:
                logger.info(f"Domain validated: {domain.domain_name}")
                return domain
            else:
                logger.warning(f"Invalid or inactive domain key attempted")
                return None
        except Exception as e:
            logger.error(f"Error validating domain key: {e}")
            return None
    
    @staticmethod
    def get_domain_from_key(domain_key: str) -> Optional[str]:
        """Extract domain name from key (if using pattern-based keys)"""
        domain_mapping = {
            "sk_live_speedoloan": "speedoloan",
            "sk_live_rupylalao": "rupylalao",
            "sk_live_5mint": "5mint"
        }
        
        for prefix, domain in domain_mapping.items():
            if domain_key.startswith(prefix):
                return domain
        return None