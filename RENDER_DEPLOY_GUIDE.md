# RENDER DEPLOYMENT GUIDE

## 1. Connect Repository
1.  Go to [Render Dashboard](https://dashboard.render.com).
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub repository.
4.  Render will automatically detect `render.yaml`.

## Manual Setup (If not using Blueprint)
If you prefer to configure manually, use these settings:
- **Build Command:** `pip install -r backend/requirements.txt`
- **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

## 2. Configure Environment Variables
Render will ask for values for the environment variables defined in `render.yaml`. Copy these from your `.env` file or Railway dashboard:

| Variable | Description |
| :--- | :--- |
| `DATABASE_URL` | Your Supabase connection string (Port 5432 or 6543) |
| `SUPABASE_URL` | Check `.env` |
| `SUPABASE_KEY` | Check `.env` (Service Role Key recommended for backend) |
| `OPENROUTER_API_KEY` | Check `.env` |
| `SECRET_KEY` | Generate a random string or copy from `.env` |
| `ALLOWED_ORIGINS` | `https://zunofrontendf.vercel.app,http://localhost:5173` |

## 3. Deploy
- Click **Apply**.
- Render will start building.
- Watch the logs for "Build successful".

## 4. Post-Deployment
- Copy the URL of your new Render service (e.g., `https://zuno-backend.onrender.com`).
- Update your Frontend Environment Variables on Vercel:
    - Set `VITE_API_BASE_URL` to the new Render URL.
    - Redeploy Frontend.
