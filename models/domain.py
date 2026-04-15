from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Domain(Base):
    __tablename__ = "domains"
    
    id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String(50), unique=True, nullable=False, index=True)
    domain_key = Column(String(255), unique=True, nullable=False, index=True)
    database_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    api_logs = relationship("APILog", back_populates="domain")

class APILog(Base):
    __tablename__ = "api_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id"))
    endpoint = Column(String(255))
    method = Column(String(10))
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))
    
    domain = relationship("Domain", back_populates="api_logs")