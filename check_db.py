# check_db.py - Clean version for MASTER_DB testing
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load .env variables
load_dotenv()

# Get MASTER_DB_URL from environment
DATABASE_URL = os.getenv("MASTER_DB_URL")

if not DATABASE_URL:
    print("❌ MASTER_DB_URL not found in .env")
    exit(1)

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("✅ Successfully connected to MASTER DB!")
        print(f"📂 Connection: {DATABASE_URL.split('@')[1].split('/')[0]}")
except Exception as e:
    print(f"❌ Connection failed: {e}")