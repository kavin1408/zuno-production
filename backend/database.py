import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL from environment variable
# If not set, defaults to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./zuno_v2.db")

# Auto-detect database type and configure accordingly
if DATABASE_URL.startswith("sqlite"):
    print(f"INFO: Using SQLite database: {DATABASE_URL}")
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    print(f"INFO: Using PostgreSQL database (Supabase)")
    # PostgreSQL configuration for production
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,         # Connection pool size
        max_overflow=10      # Max overflow connections
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
