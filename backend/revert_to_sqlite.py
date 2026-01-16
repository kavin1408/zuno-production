"""
Revert to SQLite for local development.
This is the recommended setup.
"""

import os
from pathlib import Path

def revert_to_sqlite():
    """Comment out DATABASE_URL to use SQLite."""
    
    env_path = Path(".env")
    
    # Read current .env
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Comment out DATABASE_URL
    new_lines = []
    for line in lines:
        if line.startswith('DATABASE_URL='):
            new_lines.append(f'# {line}')
            print("✓ Commented out DATABASE_URL")
        else:
            new_lines.append(line)
    
    # Write updated .env
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    
    print()
    print("✅ Reverted to SQLite!")
    print("   Local development will use SQLite")
    print("   Production (Railway) will use Supabase PostgreSQL")
    print()
    print("Next: Restart Docker")
    print("  docker-compose down && docker-compose up")

if __name__ == "__main__":
    revert_to_sqlite()
