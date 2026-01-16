# Frontend Token Recovery - Quick Fix Guide

## ✅ What Was Fixed

**File:** `frontend/src/lib/api.ts`

**Changes:**
1. Added `handle401Error()` function that:
   - Logs out user via Supabase
   - Clears localStorage
   - Redirects to `/login`

2. Created `makeRequest()` helper that:
   - Checks for valid token before making request
   - Automatically handles 401 responses
   - Provides better error messages

3. Improved all API methods (`get`, `post`, `put`, `patch`, `delete`)

---

## 🔑 Key Improvements

### Before:
```typescript
// Just logged a warning if no token
if (!token) {
    console.warn("No auth token available");
}
// Continued with request anyway ❌
```

### After:
```typescript
// Throws error and redirects if no token
if (!token) {
    console.error("No auth token - redirecting");
    await handle401Error();
    throw new Error('Authentication required');
}
```

### 401 Handling:
```typescript
// Handle 401 Unauthorized
if (res.status === 401) {
    console.error('401 Unauthorized response');
    await handle401Error(); // Logout + redirect
    throw new Error('Session expired or invalid token');
}
```

---

## 🧪 Testing

**The fix is now deployed to Vercel!**

1. **Clear your browser cache/cookies**
2. **Login again** at your Vercel URL
3. **Try onboarding** - should work now with proper token

If you still see "failed to save goals":
- Open DevTools → Console
- Look for error messages
- Check Network tab for the `/onboarding` request
- Verify Authorization header is present

---

## 📊 What Happens Now

1. **User logs in** → Supabase creates session with JWT token
2. **User goes to onboarding** → API client gets token from Supabase
3. **User submits form** → Token automatically attached to request
4. **Backend receives request** → Validates token
5. **If token valid** → Returns success
6. **If token invalid/expired** → Returns 401
7. **Frontend receives 401** → Automatically logs out and redirects to login

---

## 🚀 Deployment Status

- ✅ Code committed to git
- ✅ Pushed to GitHub
- ⏳ Vercel auto-deploying...

Check your Vercel dashboard for deployment status.
