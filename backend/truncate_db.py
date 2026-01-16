"""
Quick script to truncate all database tables without confirmation.
Use this for quick database resets during development.
"""

from sqlalchemy import create_engine, text
from database import DATABASE_URL
import sys

def truncate_database():
    """Delete all data from all tables."""
    
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            print("🗑️  Truncating database...")
            print()
            
            tables = [
                ("submissions", "DELETE FROM submissions"),
                ("task_resources", "DELETE FROM task_resources"),
                ("daily_tasks", "DELETE FROM daily_tasks"),
                ("roadmap_tasks", "DELETE FROM roadmap_tasks"),
                ("roadmaps", "DELETE FROM roadmaps"),
                ("goals", "DELETE FROM goals"),
                ("users", "DELETE FROM users"),
            ]
            
            total_deleted = 0
            for table_name, query in tables:
                result = conn.execute(text(query))
                conn.commit()
                count = result.rowcount
                total_deleted += count
                print(f"  ✓ {table_name:20} - {count:4} rows deleted")
            
            print()
            print(f"✅ Database truncated successfully!")
            print(f"   Total rows deleted: {total_deleted}")
            print()
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    truncate_database()
