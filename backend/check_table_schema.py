from sqlalchemy import create_engine, inspect
from database import DATABASE_URL
import sys

def check_schema():
    print(f"Connecting to {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    
    print("\nChecking 'users' table for 'full_name'...")
    columns = inspector.get_columns('users')
    col_names = [c['name'] for c in columns]
    if 'full_name' in col_names:
        print("✅ full_name column EXISTS")
    else:
        print("❌ full_name column MISSING")
        print(f"Found columns: {col_names}")

if __name__ == "__main__":
    check_schema()
