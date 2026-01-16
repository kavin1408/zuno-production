# 🚀 Create New Supabase Project - Step-by-Step Guide

## Overview

This guide will help you create a fresh Supabase project and migrate ZUNO to use it.

**Time Required:** 15-20 minutes

---

## Step 1: Create Supabase Project (5 minutes)

### 1.1 Go to Supabase Dashboard

Visit: https://supabase.com/dashboard

### 1.2 Create New Project

1. Click **"New Project"** button
2. Fill in details:
   - **Name:** `zuno-production`
   - **Database Password:** Click "Generate a password" and **SAVE IT**
   - **Region:** `Southeast Asia (Singapore)` or closest to you
   - **Pricing Plan:** Free

3. Click **"Create new project"**
4. Wait ~2 minutes for setup

### 1.3 Save Your Credentials

**IMPORTANT:** Copy these immediately and save to a text file:

```
Project Name: zuno-production
Project URL: https://[YOUR_PROJECT_REF].supabase.co
Database Password: [SAVE THIS - YOU WON'T SEE IT AGAIN]
```

---

## Step 2: Get API Credentials (2 minutes)

### 2.1 Get API Keys

Go to: **Settings → API**

Copy these values:

```bash
# Project URL
VITE_SUPABASE_URL=https://[YOUR_PROJECT_REF].supabase.co

# Project API keys - anon key
VITE_SUPABASE_ANON_KEY=[YOUR_ANON_KEY]

# Project API keys - service_role key (for admin operations)
SUPABASE_SERVICE_ROLE_KEY=[YOUR_SERVICE_ROLE_KEY]
```

### 2.2 Get JWT Secret

Scroll down on the same page:

```bash
# JWT Secret
SUPABASE_JWT_SECRET=[YOUR_JWT_SECRET]
```

### 2.3 Get Database Connection String

Go to: **Settings → Database**

Scroll to "Connection string" section:

Select **"URI"** tab and copy:

```bash
DATABASE_URL=postgresql://postgres.[PROJECT_REF]:[YOUR_PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
```

**Replace `[YOUR_PASSWORD]` with the database password you saved earlier!**

---

## Step 3: Update Local Frontend (1 minute)

### 3.1 Edit `frontend/.env.local`

Open the file and update:

```bash
VITE_SUPABASE_URL=https://[YOUR_PROJECT_REF].supabase.co
VITE_SUPABASE_ANON_KEY=[YOUR_ANON_KEY]
VITE_API_BASE_URL=http://localhost:8000
```

### 3.2 Edit `frontend/.env.production`

```bash
VITE_SUPABASE_URL=https://[YOUR_PROJECT_REF].supabase.co
VITE_SUPABASE_ANON_KEY=[YOUR_ANON_KEY]
VITE_API_BASE_URL=https://zuno-production-production.up.railway.app
```

---

## Step 4: Update Local Backend (1 minute)

### 4.1 Edit `backend/.env`

Update the JWT secret:

```bash
# Keep DATABASE_URL commented for local SQLite
# DATABASE_URL=postgresql://...

SUPABASE_JWT_SECRET=[YOUR_JWT_SECRET]
OPENROUTER_API_KEY=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
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

---

## Step 5: Update Vercel (2 minutes)

### 5.1 Go to Vercel Dashboard

Visit: https://vercel.com/dashboard

### 5.2 Select Your Project

Click on `zunofrontendf`

### 5.3 Update Environment Variables

Go to: **Settings → Environment Variables**

Update these three variables:

1. **VITE_SUPABASE_URL**
   - Delete old value
   - Add new: `https://[YOUR_PROJECT_REF].supabase.co`

2. **VITE_SUPABASE_ANON_KEY**
   - Delete old value
   - Add new: `[YOUR_ANON_KEY]`

3. **VITE_API_BASE_URL**
   - Keep as: `https://zuno-production-production.up.railway.app`

### 5.4 Redeploy

Go to: **Deployments** tab
- Click on latest deployment
- Click **"Redeploy"**

---

## Step 6: Update Railway (2 minutes)

### 6.1 Go to Railway Dashboard

Visit: https://railway.com/dashboard

### 6.2 Select Your Project

Click on `zuno-production`

### 6.3 Update Environment Variables

Click on **Variables** tab

Update these variables:

1. **DATABASE_URL**
   ```
   postgresql://postgres.[PROJECT_REF]:[YOUR_PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
   ```

2. **SUPABASE_JWT_SECRET**
   ```
   [YOUR_JWT_SECRET]
   ```

3. **ALLOWED_ORIGINS**
   ```
   https://zunofrontendf.vercel.app,http://localhost:5173
   ```

Railway will automatically redeploy.

---

## Step 7: Initialize Database (2 minutes)

### 7.1 Temporarily Update Local .env

Edit `backend/.env` and uncomment DATABASE_URL:

```bash
DATABASE_URL=postgresql://postgres.[PROJECT_REF]:[YOUR_PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
```

### 7.2 Run Migration

```bash
cd backend
python init_db.py
```

You should see:
```
INFO: Using PostgreSQL database (Supabase)
Creating tables...
✓ Tables created successfully
```

### 7.3 Comment Out DATABASE_URL Again

For local development, comment it back:

```bash
# DATABASE_URL=postgresql://...
```

---

## Step 8: Configure Supabase Auth (2 minutes)

### 8.1 Set Site URL

Go to: **Authentication → URL Configuration**

Set:
- **Site URL:** `https://zunofrontendf.vercel.app`

### 8.2 Add Redirect URLs

Add these:
- `https://zunofrontendf.vercel.app/**`
- `http://localhost:5173/**`

### 8.3 Configure Email Provider

Go to: **Authentication → Providers**

1. Ensure **Email** is enabled
2. For development, disable email confirmation:
   - Go to **Authentication → Settings**
   - Uncheck "Enable email confirmations"

---

## Step 9: Test Local (2 minutes)

### 9.1 Restart Backend

```bash
cd backend
docker-compose down
docker-compose up
```

### 9.2 Restart Frontend

```bash
# Press Ctrl+C in the terminal running npm dev
npm run dev
```

### 9.3 Test Signup

1. Go to http://localhost:5173
2. Click "Sign up"
3. Enter email and password
4. Should work! ✅

### 9.4 Verify in Supabase

Go to: **Authentication → Users**

You should see your new user!

---

## Step 10: Test Production (2 minutes)

### 10.1 Wait for Deployments

- Vercel: Check deployment status
- Railway: Check deployment logs

### 10.2 Test Production Site

1. Go to https://zunofrontendf.vercel.app
2. Sign up with different email
3. Complete onboarding
4. Verify everything works

---

## Verification Checklist

- [ ] New Supabase project created
- [ ] All credentials saved
- [ ] `frontend/.env.local` updated
- [ ] `frontend/.env.production` updated
- [ ] `backend/.env` updated
- [ ] Vercel environment variables updated
- [ ] Railway environment variables updated
- [ ] Database initialized (tables created)
- [ ] Supabase Auth configured
- [ ] Local signup works
- [ ] Production signup works
- [ ] User data persists

---

## Troubleshooting

### Can't Connect to Database

**Error:** Connection timeout or refused

**Fix:**
- Check DATABASE_URL is correct
- Verify password is correct (no extra spaces)
- Use port 6543 (pooler) not 5432

### Auth Errors

**Error:** Invalid JWT or auth errors

**Fix:**
- Verify SUPABASE_JWT_SECRET matches in backend
- Check VITE_SUPABASE_ANON_KEY is correct in frontend

### Vercel Deployment Fails

**Fix:**
- Ensure all environment variables are set
- Trigger manual redeploy
- Check deployment logs

---

## Quick Reference

### Credentials Template

Save this template with your actual values:

```bash
# PROJECT INFO
Project Name: zuno-production
Project URL: https://[YOUR_PROJECT_REF].supabase.co
Database Password: [YOUR_PASSWORD]

# FRONTEND (.env.local and .env.production)
VITE_SUPABASE_URL=https://[YOUR_PROJECT_REF].supabase.co
VITE_SUPABASE_ANON_KEY=[YOUR_ANON_KEY]

# BACKEND (.env)
SUPABASE_JWT_SECRET=[YOUR_JWT_SECRET]
DATABASE_URL=postgresql://postgres.[PROJECT_REF]:[YOUR_PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres

# ADMIN (optional)
SUPABASE_SERVICE_ROLE_KEY=[YOUR_SERVICE_ROLE_KEY]
```

---

**Ready to start?** Begin with Step 1 and work through each step in order!
