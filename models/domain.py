import enum
from sqlalchemy import Enum as SQLEnum 
from sqlalchemy import DECIMAL, JSON, JSON, BigInteger, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String(50), unique=True, nullable=False)
    domain_code = Column(String(100), unique=True, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    api_logs = relationship("APILog", back_populates="domain", cascade="all, delete-orphan")
    domain_features = relationship("BreDomainFeature", back_populates="domain", cascade="all, delete-orphan")
    bre_runs = relationship("BreRun", back_populates="domain", cascade="all, delete-orphan")

class DataTypeEnum(str, enum.Enum):
    number = "number"
    string = "string"
    boolean = "boolean"
    date = "date"


class BreFeature(Base):
    __tablename__ = "bre_features"
    id = Column(Integer, primary_key=True, index=True)
    feature_code = Column(String(100), unique=True, nullable=False)
    feature_name = Column(String(150), nullable=False)
    data_type = Column(SQLEnum(DataTypeEnum), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    domain_features = relationship("BreDomainFeature", back_populates="feature")






class BreDomainFeature(Base):
    __tablename__ = "bre_domain_features"

    id = Column(Integer, primary_key=True, index=True)

    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=False)
    feature_id = Column(Integer, ForeignKey("bre_features.id", ondelete="CASCADE"), nullable=False)
    operator = Column(String(20))   # >, <, =, BETWEEN, IN
    value_from = Column(String(100))
    value_to = Column(String(100))
    value_text = Column(String(255))
    score_weight = Column(DECIMAL(10, 2))
    target_decile_id = Column(Integer, ForeignKey("bre_deciles.id", ondelete="SET NULL"))
    feature_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    # Relationships
    domain = relationship("Domain", back_populates="domain_features")
    feature = relationship("BreFeature", back_populates="domain_features")
    decile = relationship("BreDecile")



class BreDecile(Base):
    __tablename__ = "bre_deciles"
    id = Column(Integer, primary_key=True, index=True)
    decile_no = Column(Integer, unique=True, nullable=False)
    decile_code = Column(String(20), unique=True, nullable=False)
    risk_band = Column(String(50))      # LOW / MEDIUM / HIGH
    decision = Column(String(50))       # APPROVE / REJECT / REVIEW
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())



class BreRun(Base):
    __tablename__ = "bre_runs"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"))
    final_decile_id = Column(Integer, ForeignKey("bre_deciles.id", ondelete="SET NULL"))
    final_decision = Column(String(50))
    total_score = Column(DECIMAL(10, 2))
    matched_feature_count = Column(Integer)
    input_payload = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    # Relationships
    domain = relationship("Domain", back_populates="bre_runs")
    final_decile = relationship("BreDecile")
    feature_results = relationship("BreRunFeatureResult", back_populates="bre_run", cascade="all, delete-orphan")

class BreRunFeatureResult(Base):
    __tablename__ = "bre_run_feature_results"
    id = Column(Integer, primary_key=True, index=True)
    bre_run_id = Column(Integer, ForeignKey("bre_runs.id", ondelete="CASCADE"))
    feature_id = Column(Integer, ForeignKey("bre_features.id"))
    customer_value = Column(String(100))
    operator = Column(String(20))
    expected_value = Column(String(100))
    is_matched = Column(Boolean)
    score_awarded = Column(DECIMAL(10, 2))
    created_at = Column(DateTime, server_default=func.now())
    # Relationships
    bre_run = relationship("BreRun", back_populates="feature_results")
    feature = relationship("BreFeature")


class APILog(Base):
    __tablename__ = "api_logs"
    id = Column(Integer, primary_key=True)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"))
    request = Column(JSON)
    response = Column(JSON)
    status_code = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    domain = relationship("Domain", back_populates="api_logs")