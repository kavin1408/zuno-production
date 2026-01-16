"""
Initialize database with corrected connection string.
Using direct connection instead of pooler for initialization.
"""

from sqlalchemy import create_engine
from models import Base

# Direct connection (port 5432) for database initialization
DB_URL = "postgresql://postgres:Kwp6Co2r4OU5KCHV@db.frmzwunvythvziqyfwxy.supabase.co:5432/postgres"

def init_database():
    """Create all tables in new Supabase database."""
    
    print("🔄 Initializing New Supabase Database")
    print("=" * 60)
    print()
    print(f"Project: frmzwunvythvziqyfwxy")
    print(f"Using direct connection (port 5432)")
    print()
    
    try:
        # Create engine
        print("Connecting to database...")
        engine = create_engine(DB_URL, pool_pre_ping=True)
        
        # Test connection
        with engine.connect() as conn:
            print("✓ Connection successful!")
        
        # Create all tables
        print()
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        print()
        print("✅ Database initialized successfully!")
        print()
        print("Tables created:")
        for table in Base.metadata.sorted_tables:
            print(f"  ✓ {table.name}")
        
        print()
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Troubleshooting:")
        print("- Check database password is correct")
        print("- Verify Supabase project is active")
        print("- Ensure network connection is stable")
        print()
        return False

if __name__ == "__main__":
    success = init_database()
    
    if success:
        print("=" * 60)
        print("DATABASE READY!")
        print("=" * 60)
        print()
        print("Next: Update Vercel and Railway")
        print("Run: python print_deployment_steps.py")
        print()
