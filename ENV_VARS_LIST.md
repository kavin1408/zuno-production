# Required Environment Variables for Render

Copy these values from your Railway Dashboard or `.env` file and paste them into Render's "Environment" tab.

| Key | Value (Example/Source) |
| :--- | :--- |
| `DATABASE_URL` | `postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres` (Use the connection string from Supabase > Settings > Database > Connection Pooling (Transaction Mode is best usually, but Session is fine if port is 5432)) |
| `SUPABASE_URL` | `https://[PROJECT_REF].supabase.co` |
| `SUPABASE_KEY` | `eyJ...` (Your `service_role` key is recommended for backend, or `anon` key if permissions allow) |
| `OPENROUTER_API_KEY` | `sk-or-v1-...` |
| `SECRET_KEY` | `[RANDOM_STRING]` (Generate one: `openssl rand -hex 32`) |
| `ALLOWED_ORIGINS` | `https://zuno-v2.vercel.app` (Add `http://localhost:5173` for dev) |
