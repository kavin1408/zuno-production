"""
Fix Supabase connection - use direct connection instead of pooler for local dev.
"""

import os
from pathlib import Path

# Supabase direct connection (port 5432 for local development)
SUPABASE_URL = "postgresql://postgres:x25CeFZHyZ9S6dE0@db.dcjsmglxckhllafocexe.supabase.co:5432/postgres"

def fix_connection():
    """Update .env with correct Supabase connection."""
    
    env_path = Path(".env")
    
    # Read current .env
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update DATABASE_URL
    new_lines = []
    for line in lines:
        if line.startswith('DATABASE_URL='):
            new_lines.append(f'DATABASE_URL={SUPABASE_URL}\n')
            print("✓ Updated DATABASE_URL to use direct connection (port 5432)")
        else:
            new_lines.append(line)
    
    # Write updated .env
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    
    print()
    print("✅ Connection string fixed!")
    print(f"   Using: Direct connection (port 5432)")
    print()
    print("Next: Restart Docker")
    print("  docker-compose down && docker-compose up -d")

if __name__ == "__main__":
    fix_connection()
