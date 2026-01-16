# 🚨 The Final Fix: Secret Mismatch

The error "Session expired or invalid token" typically happens for one reason:

**The Backend (Railway) is using the WRONG secret to verify the token.**

Common Mistake: Copying the **Anon Key** instead of the **JWT Secret**.

## 🛑 STOP and Check This EXACTLY

1.  **Go to Supabase Dashboard**
    *   Settings (Cog icon) -> **API**
    *   Scroll down to **JWT Settings**
    *   Look at **JWT Secret**
    *   Does it start with `eyJ...`? **NO.** It should be a random string like `3f4...2a1`.
    *   **COPY THIS SECRET.**

2.  **Go to Railway Dashboard**
    *   Click your Project -> **Variables**.
    *   Find `SUPABASE_JWT_SECRET`.
    *   **Is it `eyJ...`?**
    *   **IF YES -> THAT IS WRONG!** You pasted the Anon Key! ❌
    *   **Click Edit** and Paste the random string from Step 1. ✅

3.  **Redeploy**
    *   Railway should auto-redeploy when you save.

---

## 🧹 After Redeploy (Verification)

1.  Go to `https://zuno-v2.vercel.app/`
2.  **Clear Site Data** (F12 -> Application -> Storage -> Clear site data).
3.  Login.
4.  Onboarding should now work.

**Why this matters:**
- **Anon Key**: Identifying the app (Public).
- **JWT Secret**: Signing the user's session (Private).
- If Railway uses the Anon Key to verify the User Session, it fails immediately.
