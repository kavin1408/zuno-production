# 🛠️ 401 Unauthorized Recovery Guide

If you are seeing "Session expired or invalid token" during onboarding, it's because your browser is still holding an **old session token** from the previous Supabase project. The backend has the new secret and cannot verify your old token.

## Step-by-Step Recovery

### 1. Force Logout & Clear Browser Data (Crucial)
Your browser is likely trying to use a token that no longer exists in the new Supabase project.

1. Open http://localhost:5173 
2. Open **Developer Tools** (Press `F12` or `Ctrl+Shift+I`)
3. Go to the **Application** tab (at the top of DevTools)
4. Select **Local Storage** on the left sidebar
5. Right-click on `http://localhost:5173` and click **Clear**
6. Select **Cookies** on the left sidebar
7. Right-click on `http://localhost:5173` and click **Clear**
8. **Hard Refresh** the page by pressing `Ctrl + Shift + R`

### 2. Sign Up Again
Since we switched to a **new project**, your old account doesn't exist anymore.

1. Go to the **Sign Up** page
2. Create a **new account** (you can use the same email, it's a fresh database)
3. Complete the onboarding flow

### 3. Verify the Fix
Once you sign up again, the application will generate a **new token** compatible with the new secret.

---

## Why this happened
When we migrated to the new Supabase project:
1. We generated a **new JWT Secret**.
2. We updated the **Backend** to use this new secret.
3. Your browser was still logged in with a token signed by the **old secret**.
4. When you sent that old token to the backend, it failed verification (401).

**Clearing Local Storage forces the app to get a fresh, valid token.**
