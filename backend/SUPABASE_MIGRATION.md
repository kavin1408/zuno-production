# Supabase PostgreSQL Migration Guide

## What This Does

Switches your local development from SQLite to Supabase PostgreSQL database.

**Benefits:**
- ✅ Same database for local and production
- ✅ No more auth sync issues
- ✅ Consistent data across environments
- ✅ Test with real PostgreSQL features

---

## Step 1: Update backend/.env

Add this line to `backend/.env`:

```bash
DATABASE_URL=postgresql://postgres.dcjsmglxckhllafocexe:x25CeFZHyZ9S6dE0@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

**Important:** Use port **6543** (Connection Pooler) not 5432 for better performance.

---

## Step 2: Restart Docker Backend

```bash
cd backend
docker-compose down
docker-compose up
```

You should see:
```
INFO: Using PostgreSQL database (Supabase)
```

---

## Step 3: Initialize Database Schema

Run migrations to create tables:

```bash
cd backend
python init_db.py
```

This creates all tables in Supabase PostgreSQL.

---

## Step 4: Verify Connection

Test the connection:

```bash
python check_db.py
```

Should show:
```
✓ Connected to Supabase PostgreSQL
✓ Tables created
```

---

## Step 5: Test Signup

1. Go to http://localhost:5173
2. Sign up with new account
3. Should work without auth errors!

---

## Complete .env Configuration

Your `backend/.env` should have:

```bash
# Database - Supabase PostgreSQL
DATABASE_URL=postgresql://postgres.dcjsmglxckhllafocexe:x25CeFZHyZ9S6dE0@aws-0-ap-south-1.pooler.supabase.com:6543/postgres

# Authentication
SUPABASE_JWT_SECRET=4iZ15wAI823vU3hTNN2Z+Z6odhKMYNX3UCwUb3vFdegNKM08yvEcmbE7L0Dq+CbkQgW1EYLpuS3kvWfTEdL7og==

# AI Service
OPENROUTER_API_KEY=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

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Port (optional, Docker sets this)
PORT=8000
```

---

## Troubleshooting

### Connection Fails

**Error:** `could not connect to server`

**Fix:**
- Check DATABASE_URL is correct
- Ensure using port 6543 (pooler)
- Verify Supabase project is active

### Tables Not Created

**Error:** `relation does not exist`

**Fix:**
```bash
python init_db.py
```

---

## Rollback to SQLite

If you need to go back:

1. Comment out DATABASE_URL in .env:
   ```bash
   # DATABASE_URL=postgresql://...
   ```

2. Restart Docker:
   ```bash
   docker-compose down
   docker-compose up
   ```

---

**Status:** Ready to migrate!
