import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL not found in .env")
else:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    print(f"Checking schema for: {DATABASE_URL.split('@')[-1]}")
    
    try:
        engine = create_engine(DATABASE_URL)
        inspector = inspect(engine)
        
        # Get all tables
        tables = inspector.get_table_names()
        print(f"\nFound {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
        
        # Check for expected tables
        expected_tables = ['users', 'goals', 'daily_tasks', 'task_executions', 'feedback']
        print("\nExpected tables check:")
        for table in expected_tables:
            if table in tables:
                print(f"  ✓ {table} exists")
                # Show columns
                columns = inspector.get_columns(table)
                print(f"    Columns: {', '.join([col['name'] for col in columns])}")
            else:
                print(f"  ✗ {table} MISSING")
        
        # Test a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM users"))
            count = result.fetchone()[0]
            print(f"\nUsers table has {count} records")
            
    except Exception as e:
        print(f"Error checking database: {e}")
