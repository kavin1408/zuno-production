# 🧪 Manual Verification & Recovery Guide

The backend is **Active** and healthy (`{"status":"ok"}`), but you are still seeing "failed to save goals". This often happens due to browser caching or residual session issues.

## 🧹 Step 1: The "Nuclear" Clean-up (Crucial)

Browser caches often hold onto the "bad" state (old tokens, old code).

1.  Open your Zuno tab: `https://zuno-v2.vercel.app/`
2.  Open DevTools: Press `F12` or `Right Click` -> `Inspect`
3.  Go to the **Application** tab (you might need to click `>>` to see it)
4.  On the left sidebar, click **Storage**
5.  Click the button **"Clear site data"** (This clears Local Storage, Cookies, and Cache at once)
6.  **Refresh** the page (`Ctrl + R`)

## 🔁 Step 2: The Clean Test Flow

1.  **Login/Signup**: Use your email/password.
2.  **Onboarding**: 
    *   Enter Goals
    *   Select Persona
    *   Click "Generate My Plan"
3.  **Observation**:
    *   **Success**: You are redirected to the Dashboard/Daily Plan.
    *   **Failure**: You see "failed to save goals" again.

## 🕵️ Step 3: Diagnosing the "Failure" (If it happens)

If it fails after Step 1 & 2, we need to see *why*. The backend is up, so it's returning a specific error.

1.  Keep DevTools open (`F12`)
2.  Go to the **Network** tab
3.  Filter by **"Fetch/XHR"**
4.  Click "Generate My Plan" again
5.  Look for a request named `onboarding` or `daily-plan` that keeps spinning or turns **Red**.
6.  **Click on that red request**.
7.  Click the **Response** tab on the right.
    *   *What does it say?* (e.g., `{"detail": "User not found"}`, `{"error": "Database timeout"}`)

## 🛠️ Common Fixes based on Error

| Error Type | Likely Cause | Fix |
| :--- | :--- | :--- |
| **401 Unauthorized** | Old Token | **Step 1** (Clear site data) fixes this. |
| **500 Internal Error** | Backend Bug | Check Railway Logs (I can do this for you). |
| **Network Error / CORS** | Browser Block | Check Console tab for "blocked by CORS policy". |
| **404 Not Found** | Wrong URL | Frontend API URL might be wrong (we checked this, it looked good). |

**Let me know exactly what the Network Response says if it fails!**
