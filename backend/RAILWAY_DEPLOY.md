# Railway Backend Deployment Guide

## Quick Steps to Deploy Backend

### Step 1: Verify Environment Variables

Go to: https://railway.com/project/090f380f-d43b-49b1-ae85-0b021b2db780

Click on your service → **Variables** tab

**Verify these are set:**

```
DATABASE_URL=postgresql://postgres.frmzwunvythvziqyfwxy:Kwp6Co2r4OU5KCHV@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres

SUPABASE_JWT_SECRET=SXzdvsmt24m5Z4qZI1ouH8PXfckphTmd+ipQfXL+OoRU1SHyLw550OONpVJD3ztHM5mSH42OgMrVWzkQk2ImEQ==

OPENROUTER_API_KEY=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

ALLOWED_ORIGINS=https://zunofrontendf.vercel.app,http://localhost:5173
```

### Step 2: Trigger Deployment

If variables are correct:
1. Go to **Deployments** tab
2. Click **"Deploy"** or **"Redeploy"** button
3. Wait for deployment (~2-3 minutes)

If variables need updating:
1. Update the variables
2. Railway will automatically redeploy

### Step 3: Check Deployment Logs

1. Click on the running deployment
2. View logs for any errors
3. Look for: "Application startup complete"

### Step 4: Test Backend

Visit: https://zuno-production-production.up.railway.app/

Should return:
```json
{"status":"ok","message":"Zuno Backend is running"}
```

### Step 5: Test API Docs

Visit: https://zuno-production-production.up.railway.app/docs

Should show FastAPI interactive documentation

---

## Troubleshooting

### Deployment Fails

**Check logs for:**
- Database connection errors
- Missing environment variables
- Port binding issues

**Common fixes:**
- Verify DATABASE_URL password is correct
- Ensure all environment variables are set
- Check Dockerfile is present

### Database Connection Error

**Error:** `could not connect to server`

**Fix:**
- Verify DATABASE_URL is correct
- Check Supabase project is active
- Try using direct connection (port 5432) instead of pooler (6543)

### CORS Errors

**Error:** `CORS policy blocked`

**Fix:**
Update ALLOWED_ORIGINS to include:
```
https://zunofrontendf.vercel.app,http://localhost:5173
```

---

## Success Indicators

✅ Deployment status: "Success" or "Running"
✅ Health endpoint returns 200 OK
✅ API docs are accessible
✅ No errors in deployment logs
✅ Can connect to Supabase database

---

**After deployment succeeds, test the full application!**
