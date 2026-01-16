from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL not found")
    exit(1)

engine = create_engine(DATABASE_URL)

def run_migration():
    with engine.connect() as conn:
        print("Adding 'full_name' column to 'users' table...")
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR"))
            conn.commit()
            print("✓ Column 'full_name' added successfully (or already exists)")
        except Exception as e:
            print(f"❌ Error adding column: {e}")

        print("\nChecking current columns in 'users' table:")
        result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'users'"))
        for row in result:
            print(f"  - {row[0]}")

if __name__ == "__main__":
    run_migration()
