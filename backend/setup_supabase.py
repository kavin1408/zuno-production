"""
Setup script to migrate from SQLite to Supabase PostgreSQL.
This configures your local development to use the same database as production.
"""

import os
from pathlib import Path

# Supabase connection string (using Connection Pooler for better performance)
SUPABASE_URL = "postgresql://postgres.dcjsmglxckhllafocexe:x25CeFZHyZ9S6dE0@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

def setup_supabase():
    """Configure .env to use Supabase PostgreSQL."""
    
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ Error: .env file not found")
        print("Please create .env file first (copy from .env.example)")
        return False
    
    # Read current .env
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Check if DATABASE_URL already exists
    has_database_url = False
    new_lines = []
    
    for line in lines:
        if line.startswith('DATABASE_URL='):
            # Replace existing DATABASE_URL
            new_lines.append(f'DATABASE_URL={SUPABASE_URL}\n')
            has_database_url = True
            print("✓ Updated existing DATABASE_URL")
        elif line.startswith('#DATABASE_URL=') or line.startswith('# DATABASE_URL='):
            # Uncomment and update
            new_lines.append(f'DATABASE_URL={SUPABASE_URL}\n')
            has_database_url = True
            print("✓ Uncommented and updated DATABASE_URL")
        else:
            new_lines.append(line)
    
    # If DATABASE_URL doesn't exist, add it
    if not has_database_url:
        # Add after first comment block
        insert_index = 0
        for i, line in enumerate(new_lines):
            if line.strip() and not line.startswith('#'):
                insert_index = i
                break
        
        new_lines.insert(insert_index, f'DATABASE_URL={SUPABASE_URL}\n')
        new_lines.insert(insert_index + 1, '\n')
        print("✓ Added DATABASE_URL to .env")
    
    # Write updated .env
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    
    print()
    print("✅ Configuration updated successfully!")
    print(f"   Database: Supabase PostgreSQL")
    print(f"   Connection: {SUPABASE_URL[:50]}...")
    print()
    return True

def main():
    print("🔄 Migrating to Supabase PostgreSQL")
    print("=" * 50)
    print()
    
    if setup_supabase():
        print("Next steps:")
        print("1. Restart Docker: docker-compose down && docker-compose up")
        print("2. Initialize database: python init_db.py")
        print("3. Test signup at http://localhost:5173")
        print()
        print("✨ Migration complete!")
    else:
        print("❌ Migration failed")

if __name__ == "__main__":
    main()
