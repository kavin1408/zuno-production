"""
Initialize database schema in new Supabase project.
Run this after creating your new Supabase project.
"""

from sqlalchemy import create_engine
from models import Base
from database import DATABASE_URL
import sys

def init_supabase_database():
    """Create all tables in Supabase PostgreSQL."""
    
    print("🔄 Initializing Supabase Database")
    print("=" * 60)
    print()
    
    # Check if DATABASE_URL is set
    if DATABASE_URL.startswith("sqlite"):
        print("❌ Error: DATABASE_URL is not set to Supabase PostgreSQL")
        print()
        print("Please temporarily uncomment DATABASE_URL in .env:")
        print("DATABASE_URL=postgresql://postgres.[REF]:[PASSWORD]@...")
        print()
        return False
    
    print(f"Connecting to: {DATABASE_URL[:50]}...")
    print()
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Create all tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        print()
        print("✅ Database initialized successfully!")
        print()
        print("Tables created:")
        for table in Base.metadata.sorted_tables:
            print(f"  ✓ {table.name}")
        
        print()
        print("Next steps:")
        print("1. Comment out DATABASE_URL in .env (for local SQLite)")
        print("2. Configure Supabase Auth settings")
        print("3. Restart Docker: docker-compose down && docker-compose up")
        print("4. Test signup at http://localhost:5173")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Common issues:")
        print("- Check DATABASE_URL is correct")
        print("- Verify database password")
        print("- Ensure Supabase project is active")
        print()
        return False

if __name__ == "__main__":
    success = init_supabase_database()
    sys.exit(0 if success else 1)
