# Environment Configuration Guide

## Overview

The ZUNO frontend now uses environment variables to connect to different backends:
- **Local Development**: Docker backend at `http://localhost:8000`
- **Production**: Railway backend at `https://zuno-production-production.up.railway.app`

---

## Files Created

### ✅ `src/vite-env.d.ts`
TypeScript definitions for environment variables.

### ✅ `.env.production`
Production environment configuration (for Vercel deployment).

### ⚠️ `.env.local`
**You need to manually update this file** for local development.

---

## Required Action: Update `.env.local`

Open `frontend/.env.local` and change the `VITE_API_BASE_URL`:

**FROM:**
```bash
VITE_API_BASE_URL=https://zuno-production-production.up.railway.app
```

**TO:**
```bash
VITE_API_BASE_URL=http://localhost:8000
```

### Complete `.env.local` for Local Development:

```bash
VITE_SUPABASE_URL=https://dcjsmglxckhllafocexe.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjanNtZ2x4Y2tobGxhZm9jZXhlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjYwNjIwODksImV4cCI6MjA4MTYzODA4OX0.WS3PLu9JN2SxtJr_TK2oIdfwdHuKnkP3rVDUzM7zoIA
VITE_API_BASE_URL=http://localhost:8000
```

---

## How It Works

### `src/lib/api.ts`
```typescript
const BACKEND_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

This line:
1. Reads `VITE_API_BASE_URL` from environment variables
2. Falls back to `http://localhost:8000` if not set
3. Uses the URL for all API calls

### Environment Files Priority

Vite loads environment files in this order:
1. `.env.local` (local development, **highest priority**)
2. `.env.production` (production builds)
3. `.env` (default fallback)

---

## Usage

### Local Development with Docker Backend

1. **Update `.env.local`** (see above)

2. **Start Docker Backend:**
   ```bash
   cd backend
   docker-compose up
   ```

3. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Verify Connection:**
   - Open http://localhost:5173
   - Check browser console (F12)
   - Should see API calls to `http://localhost:8000`

---

### Production Deployment to Vercel

The `.env.production` file is automatically used when building for production.

**Option 1: Vercel CLI**
```bash
cd frontend
vercel --prod
```

**Option 2: Vercel Dashboard**
1. Go to Vercel project settings
2. Environment Variables
3. Add:
   ```
   VITE_SUPABASE_URL=https://dcjsmglxckhllafocexe.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   VITE_API_BASE_URL=https://zuno-production-production.up.railway.app
   ```

---

## Backend CORS Configuration

### For Local Development

Your Docker backend needs to allow requests from `localhost:5173`.

**Check `backend/.env`:**
```bash
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

If missing, add it and restart Docker:
```bash
docker-compose down
docker-compose up
```

### For Production

Railway backend needs to allow requests from your Vercel URL.

**In Railway Dashboard:**
```bash
ALLOWED_ORIGINS=https://zunofrontendf.vercel.app,http://localhost:5173
```

---

## Testing

### Test Local Connection

1. Start Docker backend
2. Start frontend dev server
3. Open browser to http://localhost:5173
4. Open DevTools (F12) → Network tab
5. Try to login/signup
6. Check API requests go to `localhost:8000`
7. Verify no CORS errors

### Test Production Connection

1. Deploy to Vercel
2. Update Railway CORS
3. Visit Vercel URL
4. Open DevTools → Network tab
5. Check API requests go to Railway URL
6. Verify no CORS errors

---

## Troubleshooting

### CORS Error in Local Development

**Error:** `Access to fetch at 'http://localhost:8000/...' has been blocked by CORS policy`

**Solution:**
1. Check `backend/.env` has `ALLOWED_ORIGINS=http://localhost:5173`
2. Restart Docker: `docker-compose down && docker-compose up`

### Frontend Still Using Old URL

**Error:** API calls going to wrong backend

**Solution:**
1. Stop frontend dev server (Ctrl+C)
2. Verify `.env.local` has correct `VITE_API_BASE_URL`
3. Restart: `npm run dev`
4. Hard refresh browser (Ctrl+Shift+R)

### Environment Variables Not Loading

**Error:** `import.meta.env.VITE_API_BASE_URL` is undefined

**Solution:**
1. Ensure variable starts with `VITE_`
2. Restart dev server after changing `.env` files
3. Check `src/vite-env.d.ts` exists

---

## Summary

✅ **Updated Files:**
- `src/lib/api.ts` - Now uses environment variable
- `src/vite-env.d.ts` - TypeScript definitions
- `.env.production` - Production configuration

⚠️ **Manual Action Required:**
- Update `frontend/.env.local` to use `http://localhost:8000`

🎯 **Result:**
- Local development connects to Docker backend
- Production deployment connects to Railway backend
- No code changes needed when switching environments
