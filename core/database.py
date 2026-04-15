from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Dict, Optional
from .config import settings, DOMAIN_DB_MAPPING
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.engines: Dict[str, any] = {}
        self.sessions: Dict[str, scoped_session] = {}
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize database engines for all domains"""
        for domain_name, db_url in DOMAIN_DB_MAPPING.items():
            try:
                engine = create_engine(
                    db_url,
                    pool_pre_ping=True,
                    pool_size=5,
                    max_overflow=10
                )
                self.engines[domain_name] = engine
                self.sessions[domain_name] = scoped_session(
                    sessionmaker(autocommit=False, autoflush=False, bind=engine)
                )
                logger.info(f"Database engine initialized for {domain_name}")
            except Exception as e:
                logger.error(f"Failed to initialize database for {domain_name}: {e}")
    
    def get_session(self, domain_name: str) -> Optional[scoped_session]:
        """Get database session for specific domain"""
        if domain_name not in self.sessions:
            logger.error(f"No database session found for domain: {domain_name}")
            return None
        return self.sessions[domain_name]
    
    def close_all(self):
        """Close all database sessions"""
        for session in self.sessions.values():
            session.remove()

# Global database manager instance
db_manager = DatabaseManager()

def get_db_session(domain_name: str):
    """Dependency to get database session"""
    session = db_manager.get_session(domain_name)
    if session is None:
        raise ValueError(f"Invalid domain: {domain_name}")
    try:
        yield session
    finally:
        session.remove()