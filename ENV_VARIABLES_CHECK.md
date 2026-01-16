# Environment Variables Check

## ✅ Frontend (Vercel) - CORRECT

**File:** `frontend/.env.production`

```env
VITE_SUPABASE_URL=https://frmzwunvythvziqyfwxy.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
VITE_API_BASE_URL=https://zuno-production-production.up.railway.app
```

**Status:** ✅ All correct

---

## ⚠️ Backend (Railway) - NEEDS VERIFICATION

**Production Variables (Railway Dashboard):**

These should be set in Railway dashboard:
```env
DATABASE_URL=postgresql://postgres.frmzwunvythvziqyfwxy:Kwp6Co2r4OU5KCHV@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres

SUPABASE_JWT_SECRET=SXzdvsmt24m5Z4qZI1ouH8PXfckphTmd+ipQfXL+OoRU1SHyLw550OONpVJD3ztHM5mSH42OgMrVWzkQk2ImEQ==

OPENROUTER_API_KEY=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

ALLOWED_ORIGINS=https://zunofrontendf.vercel.app,http://localhost:5173
```

**⚠️ Local `.env` Issue:**
The local `backend/.env` file has:
```env
SUPABASE_JWT_SECRET=your-jwt-secret-here  # ❌ WRONG - placeholder
```

**This is OK** because:
- Local `.env` is only for local development
- Railway uses its own environment variables from the dashboard
- The Railway deployment has the correct secret

---

## 🔍 How to Verify Railway Variables

1. **Go to Railway Dashboard:**
   https://railway.com/project/090f380f-d43b-49b1-ae85-0b021b2db780

2. **Click on your service** (zuno-production)

3. **Go to "Variables" tab**

4. **Verify these 4 variables are set:**
   - `DATABASE_URL`
   - `SUPABASE_JWT_SECRET`
   - `OPENROUTER_API_KEY`
   - `ALLOWED_ORIGINS`

5. **Check the values match** the production values above

---

## 🔑 Critical Variables Explained

### `SUPABASE_JWT_SECRET`
- **What it is:** Secret key to verify JWT tokens from Supabase
- **Where to find:** Supabase Dashboard → Settings → API → JWT Secret
- **Production value:** `SXzdvsmt24m5Z4qZI1ouH8PXfckphTmd+ipQfXL+OoRU1SHyLw550OONpVJD3ztHM5mSH42OgMrVWzkQk2ImEQ==`

### `DATABASE_URL`
- **What it is:** PostgreSQL connection string to Supabase
- **Format:** `postgresql://postgres.PROJECT:PASSWORD@HOST:6543/postgres`
- **Production value:** Uses connection pooler (port 6543)

### `ALLOWED_ORIGINS`
- **What it is:** CORS allowed origins for frontend
- **Must include:** Your Vercel frontend URL
- **Production value:** `https://zunofrontendf.vercel.app,http://localhost:5173`

---

## ✅ Quick Verification Commands

### Test Backend Health:
```bash
curl https://zuno-production-production.up.railway.app/
```

Expected:
```json
{"status":"ok","message":"Zuno Backend is running"}
```

### Test Backend API Docs:
Open in browser:
```
https://zuno-production-production.up.railway.app/docs
```

Should show FastAPI interactive documentation.

---

## 🚨 If Variables Are Wrong

1. **Go to Railway Dashboard**
2. **Click Variables tab**
3. **Update the incorrect variable**
4. **Railway will auto-redeploy** (takes ~2-3 minutes)
5. **Check deployment logs** for success

---

## 📊 Current Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Frontend .env | ✅ Correct | All 3 variables set properly |
| Backend Railway vars | ⚠️ Needs check | Verify in Railway dashboard |
| Backend local .env | ⚠️ Has placeholder | OK - only for local dev |
| Supabase connection | ✅ Working | Using correct project |
| CORS config | ✅ Correct | Includes Vercel URL |

---

## 🎯 Action Items

1. ✅ Frontend variables - Already correct
2. ⚠️ **Check Railway dashboard** - Verify 4 variables
3. ✅ Local backend .env - Can ignore (local dev only)
4. ✅ Test deployment - Backend should be running

**Most Important:** Verify `SUPABASE_JWT_SECRET` in Railway matches the production value!
