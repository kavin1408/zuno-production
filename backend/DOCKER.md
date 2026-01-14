# ZUNO Backend - Docker Guide

This guide explains how to run the ZUNO backend using Docker for both local development and production deployment on Railway.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)
- `.env` file configured (see `.env.example`)

## Quick Start - Local Development

### Option 1: Using Docker Compose (Recommended)

```bash
cd backend
docker-compose up
```

The backend will be available at `http://localhost:8000` with hot reload enabled.

To stop:
```bash
docker-compose down
```

### Option 2: Using Docker Directly

1. **Build the image:**
   ```bash
   cd backend
   docker build -t zuno-backend .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 --env-file .env zuno-backend
   ```

3. **Stop the container:**
   ```bash
   docker ps  # Find container ID
   docker stop <container-id>
   ```

## Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```bash
# Database (optional for local, defaults to SQLite)
DATABASE_URL=sqlite:///./zuno_v2.db

# Authentication (required)
SUPABASE_JWT_SECRET=your-supabase-jwt-secret

# AI Service (required)
OPENROUTER_API_KEY=your-openrouter-api-key

# Server (optional, defaults to 8000)
PORT=8000

# CORS (optional for local)
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

See `.env.example` for detailed documentation.

## Production Deployment on Railway

### Step 1: Prepare Your Repository

Ensure your code is pushed to GitHub with:
- `Dockerfile` in the `backend` directory
- `.env.example` for reference (never commit `.env`)

### Step 2: Create Railway Project

1. Go to [Railway.app](https://railway.app/)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your ZUNO repository
5. Railway will auto-detect the Dockerfile

### Step 3: Configure Environment Variables

In the Railway dashboard, add these environment variables:

```bash
DATABASE_URL=postgresql://user:password@host:port/database
SUPABASE_JWT_SECRET=your-actual-jwt-secret
OPENROUTER_API_KEY=your-actual-api-key
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

**Important:** 
- `PORT` is automatically set by Railway - don't override it
- Use your Supabase PostgreSQL connection string for `DATABASE_URL`
- Add your Vercel frontend URL to `ALLOWED_ORIGINS`

### Step 4: Configure Root Directory (Important!)

Since the Dockerfile is in the `backend` directory:

1. Go to Settings → Deploy
2. Set **Root Directory** to `backend`
3. Save changes

### Step 5: Deploy

Railway will automatically:
1. Detect the Dockerfile
2. Build the Docker image
3. Deploy the container
4. Assign a public URL

### Step 6: Verify Deployment

1. Check deployment logs for errors
2. Visit the Railway-provided URL
3. Test the health endpoint: `https://your-app.railway.app/`
4. Expected response: `{"status": "ok", "message": "Zuno Backend is running"}`

## Database Configuration

### Local Development (SQLite)

By default, the backend uses SQLite for local development:
- No `DATABASE_URL` needed
- Database file: `zuno_v2.db`
- Automatic table creation on startup

### Production (PostgreSQL/Supabase)

For Railway deployment:
1. Get your Supabase connection string:
   - Go to Supabase Dashboard → Project Settings → Database
   - Copy the "Connection string" (use Connection Pooler for production)
2. Set `DATABASE_URL` in Railway environment variables
3. The backend automatically detects PostgreSQL and configures connection pooling

## Troubleshooting

### Container won't start

**Check logs:**
```bash
docker logs <container-id>
```

**Common issues:**
- Missing environment variables (check `.env` file)
- Port already in use (change `PORT` in `.env`)
- Database connection failed (verify `DATABASE_URL`)

### CORS errors in production

Ensure `ALLOWED_ORIGINS` includes your frontend URL:
```bash
ALLOWED_ORIGINS=https://your-app.vercel.app,http://localhost:5173
```

### Database connection errors on Railway

- Verify `DATABASE_URL` is correct
- Use Supabase Connection Pooler (port 6543) for production
- Check Supabase IP allowlist settings

### Hot reload not working with docker-compose

Ensure volume mounts are correct in `docker-compose.yml`:
```yaml
volumes:
  - ./:/app
```

## Advanced Usage

### Running with PostgreSQL locally

Uncomment the `postgres` service in `docker-compose.yml`:

```yaml
postgres:
  image: postgres:15-alpine
  environment:
    POSTGRES_USER: zuno
    POSTGRES_PASSWORD: zuno_dev_password
    POSTGRES_DB: zuno_db
  ports:
    - "5432:5432"
```

Then update `.env`:
```bash
DATABASE_URL=postgresql://zuno:zuno_dev_password@postgres:5432/zuno_db
```

### Building for production locally

```bash
docker build -t zuno-backend:production .
docker run -p 8000:8000 --env-file .env.production zuno-backend:production
```

### Viewing container logs

```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f <container-id>
```

## Health Checks

The Docker image includes a health check that runs every 30 seconds:

```bash
# Check container health
docker ps

# Manually test health endpoint
curl http://localhost:8000/
```

## Security Best Practices

1. **Never commit `.env` files** - Use `.env.example` as template
2. **Use non-root user** - Dockerfile already configured
3. **Keep dependencies updated** - Regularly update `requirements.txt`
4. **Restrict CORS origins** - Only allow your frontend domains
5. **Use secrets management** - Railway encrypts environment variables

## Support

For issues:
1. Check Railway deployment logs
2. Verify environment variables
3. Test locally with Docker first
4. Review Supabase connection settings

---

**One Command Deployment:**
```bash
docker run -p 8000:8000 --env-file .env zuno-backend
```
