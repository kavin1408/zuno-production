# Railway JWT Secret Fix - Step-by-Step Guide

## 🎯 What You Need to Do

Update the `SUPABASE_JWT_SECRET` in your Railway deployment.

---

## 📋 Step-by-Step Instructions

### Step 1: Open Railway Dashboard

Click this link: **https://railway.com/project/090f380f-d43b-49b1-ae85-0b021b2db780**

### Step 2: Select Your Service

- You should see your service (likely named "zuno-production" or similar)
- Click on it to open the service details

### Step 3: Go to Variables Tab

- In the service view, click on the **"Variables"** tab at the top

### Step 4: Find or Add SUPABASE_JWT_SECRET

Look for a variable named `SUPABASE_JWT_SECRET`

**If it exists:**
- Click on it to edit
- Replace the value

**If it doesn't exist:**
- Click **"+ New Variable"**
- Name: `SUPABASE_JWT_SECRET`

### Step 5: Set the Correct Value

**Copy and paste this EXACT value:**

```
SXzdvsmt24m5Z4qZI1ouH8PXfckphTmd+ipQfXL+OoRU1SHyLw550OONpVJD3ztHM5mSH42OgMrVWzkQk2ImEQ==
```

⚠️ **CRITICAL:** Make sure there are NO extra spaces before or after the value!

### Step 6: Save the Variable

- Click **"Add"** or **"Update"** button
- Railway will automatically trigger a new deployment

### Step 7: Wait for Deployment

- Go to the **"Deployments"** tab
- You'll see a new deployment starting
- Wait for it to show **"Success"** (usually 2-3 minutes)

### Step 8: Verify the Fix

**Test the backend:**
```bash
curl https://zuno-production-production.up.railway.app/
```

Should return:
```json
{"status":"ok","message":"Zuno Backend is running"}
```

**Test the full app:**
1. Go to https://zuno-v2.vercel.app/
2. Clear browser cache/cookies (Ctrl+Shift+Delete)
3. Login or signup
4. Try to complete onboarding
5. Should work without 401 errors!

---

## ✅ Verification Checklist

After Railway redeploys:

- [ ] Backend health check returns 200 OK
- [ ] Login works on frontend
- [ ] Onboarding completes without 401 errors
- [ ] Dashboard loads successfully
- [ ] No "Session expired" errors in console

---

## 🔍 How to Verify the Secret is Correct

If you want to double-check the JWT secret:

1. Go to Supabase Dashboard: https://supabase.com/dashboard/project/frmzwunvythvziqyfwxy/settings/api
2. Scroll down to **"JWT Settings"**
3. Look for **"JWT Secret"**
4. It should match the value you just set in Railway

---

## 🚨 If It Still Doesn't Work

1. **Check Railway Logs:**
   - Go to Deployments tab
   - Click on the latest deployment
   - Look for errors like "SUPABASE_JWT_SECRET is not set"

2. **Verify All Environment Variables:**
   Make sure these are also set in Railway:
   - `DATABASE_URL`
   - `OPENROUTER_API_KEY`
   - `ALLOWED_ORIGINS`

3. **Check for Typos:**
   - The secret must be EXACTLY as shown above
   - No extra spaces, no line breaks

---

## 📊 Expected Result

**Before Fix:**
```
GET /daily-plan → 401 Unauthorized
Error: {"detail":"Session expired or invalid token"}
```

**After Fix:**
```
GET /daily-plan → 200 OK
Returns daily plan data successfully
```

---

## ⏱️ Timeline

- Variable update: Instant
- Railway redeploy: 2-3 minutes
- Testing: 1-2 minutes
- **Total time: ~5 minutes**

---

## 🎉 Success Indicators

You'll know it's fixed when:
1. ✅ No 401 errors in browser console
2. ✅ Onboarding completes successfully
3. ✅ Dashboard loads with data
4. ✅ Railway logs show "JWT verified successfully"
