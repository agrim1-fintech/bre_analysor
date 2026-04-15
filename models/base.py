# models/base.py
from sqlalchemy.orm import declarative_base

# This is the single source of truth for all your models
Base = declarative_base()