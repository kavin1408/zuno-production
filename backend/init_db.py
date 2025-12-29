import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL not found in .env")
else:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    print(f"Creating tables in: {DATABASE_URL.split('@')[-1]}")
    
    try:
        engine = create_engine(DATABASE_URL)
        
        # Create all tables defined in models.py
        Base.metadata.create_all(bind=engine)
        
        print("✓ All tables created successfully!")
        print("\nTables created:")
        print("  - users")
        print("  - goals")
        print("  - daily_tasks")
        print("  - submissions")
        
    except Exception as e:
        print(f"Error creating tables: {e}")
