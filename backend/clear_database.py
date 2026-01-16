"""
Script to delete all data from Supabase database tables.
This will clear all users, goals, tasks, and submissions.
"""

from sqlalchemy import create_engine, text
from database import DATABASE_URL
import sys

def clear_all_data():
    """Delete all data from all tables in the correct order (respecting foreign keys)."""
    
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            print("Starting database cleanup...")
            
            # Delete in order to respect foreign key constraints
            # 1. Delete submissions first (depends on daily_tasks)
            result = conn.execute(text("DELETE FROM submissions"))
            conn.commit()
            print(f"✓ Deleted {result.rowcount} submissions")
            
            # 2. Delete task_resources (depends on daily_tasks and roadmap_tasks)
            result = conn.execute(text("DELETE FROM task_resources"))
            conn.commit()
            print(f"✓ Deleted {result.rowcount} task resources")
            
            # 3. Delete daily_tasks (depends on users, goals, and roadmap_tasks)
            result = conn.execute(text("DELETE FROM daily_tasks"))
            conn.commit()
            print(f"✓ Deleted {result.rowcount} daily tasks")
            
            # 4. Delete roadmap_tasks (depends on roadmaps)
            result = conn.execute(text("DELETE FROM roadmap_tasks"))
            conn.commit()
            print(f"✓ Deleted {result.rowcount} roadmap tasks")
            
            # 5. Delete roadmaps (depends on users and goals)
            result = conn.execute(text("DELETE FROM roadmaps"))
            conn.commit()
            print(f"✓ Deleted {result.rowcount} roadmaps")
            
            # 6. Delete goals (depends on users)
            result = conn.execute(text("DELETE FROM goals"))
            conn.commit()
            print(f"✓ Deleted {result.rowcount} goals")
            
            # 7. Delete users (no dependencies)
            result = conn.execute(text("DELETE FROM users"))
            conn.commit()
            print(f"✓ Deleted {result.rowcount} users")
            
            print("\n✅ Database cleared successfully! All data has been deleted.")
            print("You can now start fresh with new data.")
            
            
    except Exception as e:
        print(f"\n❌ Error clearing database: {e}")
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    # Ask for confirmation
    print("⚠️  WARNING: This will delete ALL data from the database!")
    print("Tables to be cleared:")
    print("  - users")
    print("  - goals")
    print("  - roadmaps")
    print("  - roadmap_tasks")
    print("  - daily_tasks")
    print("  - task_resources")
    print("  - submissions")
    response = input("\nAre you sure you want to continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        clear_all_data()
    else:
        print("Operation cancelled.")
