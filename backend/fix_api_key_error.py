"""
Fix Invalid API Key Error
This script will create/update frontend/.env.local with correct credentials
"""

from pathlib import Path

# Correct credentials for new Supabase project
CORRECT_CREDENTIALS = """VITE_SUPABASE_URL=https://frmzwunvythvziqyfwxy.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZybXp3dW52eXRodnppcXlmd3h5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc4NzQ1NzQsImV4cCI6MjA4MzQ1MDU3NH0.Y5wxa6nLZNh8q0Nu8pzc8N98XTZr9Uu4OGD_IqswM94
VITE_API_BASE_URL=http://localhost:8000
"""

def fix_frontend_env():
    """Update frontend/.env.local with correct credentials."""
    
    env_local_path = Path("../frontend/.env.local")
    
    print("🔧 Fixing Invalid API Key Error")
    print("=" * 60)
    print()
    
    # Write correct credentials
    with open(env_local_path, 'w') as f:
        f.write(CORRECT_CREDENTIALS)
    
    print("✅ Updated frontend/.env.local with correct credentials")
    print()
    print("New Supabase Project:")
    print("  URL: https://frmzwunvythvziqyfwxy.supabase.co")
    print("  Project ID: frmzwunvythvziqyfwxy")
    print()
    print("=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print()
    print("1. Restart frontend dev server:")
    print("   - Press Ctrl+C in terminal")
    print("   - Run: npm run dev")
    print()
    print("2. Hard refresh browser:")
    print("   - Press Ctrl+Shift+R")
    print()
    print("3. Try logging in again")
    print()
    print("If still getting errors, check:")
    print("- Backend is running (docker-compose up)")
    print("- Backend has correct JWT secret")
    print()

if __name__ == "__main__":
    fix_frontend_env()
