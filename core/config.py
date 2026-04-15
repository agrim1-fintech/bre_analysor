from pydantic_settings import BaseSettings
from typing import Dict
import os

class Settings(BaseSettings):
    # Master database (for domain configuration)
    MASTER_DB_URL: str = "mysql+pymysql://root:root@127.0.0.1:3306/master_db"
    # Domain databases
    # SPEEDOLOAN_DB_URL: str = "mysql+pymysql://user:password@localhost/speedoloan_db"
    # RUPYLALAO_DB_URL: str = "mysql+pymysql://user:password@localhost/rupylalao_db"
    # FIVEMINT_DB_URL: str = "mysql+pymysql://user:password@localhost/5mint_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Domain database mapping
DOMAIN_DB_MAPPING = {
    "master": settings.MASTER_DB_URL,
    # "speedoloan": settings.SPEEDOLOAN_DB_URL,
    # "rupylalao": settings.RUPYLALAO_DB_URL,
    # "5mint": settings.FIVEMINT_DB_URL
}