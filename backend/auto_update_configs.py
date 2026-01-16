"""
Auto-update all configuration files with new Supabase credentials.
This script uses the credentials extracted from the browser.
"""

import re
from pathlib import Path

# New Supabase credentials from browser extraction
CREDENTIALS = {
    'url': 'https://frmzwunvythvziqyfwxy.supabase.co',
    'project_ref': 'frmzwunvythvziqyfwxy',
    'anon_key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZybXp3dW52eXRodnppcXlmd3h5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc4NzQ1NzQsImV4cCI6MjA4MzQ1MDU3NH0.Y5wxa6nLZNh8q0Nu8pzc8N98XTZr9Uu4OGD_IqswM94',
    'service_role_key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZybXp3dW52eXRodnppcXlmd3h5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Nzg3NDU3NCwiZXhwIjoyMDgzNDUwNTc0fQ.q9bc104zKRYN-2uv2lvxx8v4GDt9_YEL0h7-JQezedc',
    'jwt_secret': 'SXzdvsmt24m5Z4qZI1ouH8PXfckphTmd+ipQfXL+OoRU1SHyLw550OONpVJD3ztHM5mSH42OgMrVWzkQk2ImEQ==',
    'db_password': 'Kwp6Co2r4OU5KCHV',
    'db_host': 'db.frmzwunvythvziqyfwxy.supabase.co',
}

def update_file(path, updates):
    """Update file with regex replacements."""
    if not path.exists():
        print(f"⚠️  {path} not found, skipping")
        return False
    
    with open(path, 'r') as f:
        content = f.read()
    
    for pattern, replacement in updates:
        content = re.sub(pattern, replacement, content)
    
    with open(path, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated {path}")
    return True

def main():
    print("🔄 Updating all configuration files...")
    print("=" * 60)
    print()
    
    # Update frontend/.env.local
    update_file(
        Path("../frontend/.env.local"),
        [
            (r'VITE_SUPABASE_URL=.*', f'VITE_SUPABASE_URL={CREDENTIALS["url"]}'),
            (r'VITE_SUPABASE_ANON_KEY=.*', f'VITE_SUPABASE_ANON_KEY={CREDENTIALS["anon_key"]}'),
        ]
    )
    
    # Update frontend/.env.production
    update_file(
        Path("../frontend/.env.production"),
        [
            (r'VITE_SUPABASE_URL=.*', f'VITE_SUPABASE_URL={CREDENTIALS["url"]}'),
            (r'VITE_SUPABASE_ANON_KEY=.*', f'VITE_SUPABASE_ANON_KEY={CREDENTIALS["anon_key"]}'),
        ]
    )
    
    # Update backend/.env
    update_file(
        Path(".env"),
        [
            (r'SUPABASE_JWT_SECRET=.*', f'SUPABASE_JWT_SECRET={CREDENTIALS["jwt_secret"]}'),
        ]
    )
    
    # Create backend/.env.production
    db_url = f"postgresql://postgres.{CREDENTIALS['project_ref']}:{CREDENTIALS['db_password']}@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
    
    production_env = f"""# Production Environment Variables for Railway
# Auto-generated with new Supabase project credentials

DATABASE_URL={db_url}
SUPABASE_JWT_SECRET={CREDENTIALS['jwt_secret']}
OPENROUTER_API_KEY=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
ALLOWED_ORIGINS=https://zunofrontendf.vercel.app,http://localhost:5173
"""
    
    with open(Path(".env.production"), 'w') as f:
        f.write(production_env)
    
    print("✓ Created .env.production")
    
    print()
    print("✅ All local files updated successfully!")
    print()
    print("=" * 60)
    print("CREDENTIALS SUMMARY")
    print("=" * 60)
    print()
    print(f"Project URL: {CREDENTIALS['url']}")
    print(f"Project Ref: {CREDENTIALS['project_ref']}")
    print(f"Database Password: {CREDENTIALS['db_password']}")
    print()

if __name__ == "__main__":
    main()
