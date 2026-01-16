"""
Print exact commands for Vercel and Railway deployment.
"""

CREDENTIALS = {
    'url': 'https://frmzwunvythvziqyfwxy.supabase.co',
    'project_ref': 'frmzwunvythvziqyfwxy',
    'anon_key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZybXp3dW52eXRodnppcXlmd3h5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc4NzQ1NzQsImV4cCI6MjA4MzQ1MDU3NH0.Y5wxa6nLZNh8q0Nu8pzc8N98XTZr9Uu4OGD_IqswM94',
    'jwt_secret': 'SXzdvsmt24m5Z4qZI1ouH8PXfckphTmd+ipQfXL+OoRU1SHyLw550OONpVJD3ztHM5mSH42OgMrVWzkQk2ImEQ==',
    'db_password': 'Kwp6Co2r4OU5KCHV',
}

print()
print("=" * 70)
print("NEXT STEPS - DEPLOYMENT UPDATES")
print("=" * 70)
print()

print("📌 STEP 1: UPDATE VERCEL ENVIRONMENT VARIABLES")
print("-" * 70)
print()
print("Go to: https://vercel.com/dashboard")
print("→ Select 'zunofrontendf' project")
print("→ Settings → Environment Variables")
print()
print("Update these 2 variables:")
print()
print(f"VITE_SUPABASE_URL")
print(f"{CREDENTIALS['url']}")
print()
print(f"VITE_SUPABASE_ANON_KEY")
print(f"{CREDENTIALS['anon_key']}")
print()
print("Then: Deployments → Click latest → Redeploy")
print()

print("=" * 70)
print()

print("📌 STEP 2: UPDATE RAILWAY ENVIRONMENT VARIABLES")
print("-" * 70)
print()
print("Go to: https://railway.com/dashboard")
print("→ Select 'zuno-production' project")
print("→ Variables tab")
print()
print("Update these 2 variables:")
print()
print(f"DATABASE_URL")
db_url = f"postgresql://postgres.{CREDENTIALS['project_ref']}:{CREDENTIALS['db_password']}@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
print(f"{db_url}")
print()
print(f"SUPABASE_JWT_SECRET")
print(f"{CREDENTIALS['jwt_secret']}")
print()
print("Railway will automatically redeploy")
print()

print("=" * 70)
print()

print("✅ After updating Vercel and Railway, run:")
print("   python init_new_database.py")
print()
