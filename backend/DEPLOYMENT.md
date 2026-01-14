# ZUNO Backend - Quick Deployment Reference

## 🚀 One-Command Deployment

```bash
docker run -p 8000:8000 --env-file .env zuno-backend
```

---

## 📋 Quick Start Guide

### Local Development

```bash
cd backend
docker-compose up
```

Access at: `http://localhost:8000`

### Build Docker Image

```bash
cd backend
docker build -t zuno-backend .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env zuno-backend
```

---

## 🌐 Railway Deployment Steps

### 1. Configure Railway Project
- Connect GitHub repository
- Set **Root Directory** to `backend` in Settings → Deploy

### 2. Set Environment Variables

```bash
DATABASE_URL=postgresql://user:password@host:6543/database
SUPABASE_JWT_SECRET=your-jwt-secret
OPENROUTER_API_KEY=your-api-key
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

> **Note:** Railway sets `PORT` automatically - don't override it

### 3. Deploy
Railway auto-detects Dockerfile and deploys automatically.

### 4. Verify
Test health endpoint: `https://your-app.railway.app/`

Expected response:
```json
{"status": "ok", "message": "Zuno Backend is running"}
```

---

## 📁 Files Created

- `Dockerfile` - Production-ready container configuration
- `.dockerignore` - Build optimization
- `docker-compose.yml` - Local development setup
- `DOCKER.md` - Comprehensive documentation
- Updated `database.py` - SQLite/PostgreSQL auto-detection
- Updated `main.py` - Container-compatible server config
- Updated `requirements.txt` - Version pinning + gunicorn
- Updated `.env.example` - Complete environment variable reference

---

## 🔧 Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `DATABASE_URL` | No | SQLite | Database connection |
| `SUPABASE_JWT_SECRET` | Yes | - | Authentication |
| `OPENROUTER_API_KEY` | Yes | - | AI service |
| `PORT` | No | 8000 | Server port |
| `ALLOWED_ORIGINS` | No | localhost | CORS origins |

---

## ✅ Validation Results

- ✅ Docker build: **SUCCESS** (178.9s)
- ✅ Image size: Optimized (Python 3.11-slim)
- ✅ Security: Non-root user
- ✅ Health checks: Configured
- ✅ Railway compatible: Verified

---

## 📖 Full Documentation

See [DOCKER.md](file:///c:/Users/Administrator/Desktop/final%20thing/backend/DOCKER.md) for:
- Detailed deployment instructions
- Troubleshooting guide
- Advanced configuration
- Security best practices

---

## 🎯 Key Features

- **Flexible Database**: Auto-switches between SQLite (local) and PostgreSQL (production)
- **Railway Ready**: Zero-config deployment with Dockerfile auto-detection
- **Hot Reload**: Development mode with live code updates
- **Production Optimized**: Connection pooling, health checks, security hardening
- **One Command**: `docker run zuno-backend` - that's it!

---

**Need Help?** Check [DOCKER.md](file:///c:/Users/Administrator/Desktop/final%20thing/backend/DOCKER.md) for comprehensive troubleshooting and deployment guides.
