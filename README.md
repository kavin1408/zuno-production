# ZUNO - AI-Powered Learning Platform

> Your personalized AI learning companion that transforms YouTube content into structured learning paths

[![Production](https://img.shields.io/badge/Frontend-Vercel-black)](https://zunofrontendf.vercel.app)
[![Backend](https://img.shields.io/badge/Backend-Railway-purple)](https://zuno-production-production.up.railway.app)
[![Database](https://img.shields.io/badge/Database-Supabase-green)](https://supabase.com)

---

## 🎯 Overview

ZUNO is a full-stack web application that helps users learn effectively by:
- 🎓 Creating personalized learning roadmaps
- 📹 Curating relevant YouTube educational content
- 🤖 Providing AI-powered mentorship and guidance
- 📊 Tracking progress with daily tasks and quizzes
- ✅ Validating learning through interactive assessments

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      PRODUCTION                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Frontend (Vercel)        Backend (Railway)             │
│  React + Vite      ──────▶ FastAPI + Docker             │
│  zunofrontendf             zuno-production              │
│  .vercel.app               .up.railway.app              │
│                            Supabase PostgreSQL          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Tech Stack

### Frontend
- **Framework:** React 18 + Vite
- **UI Library:** Radix UI + Material-UI
- **Styling:** Tailwind CSS 4
- **State Management:** React Hooks
- **Authentication:** Supabase Auth
- **Routing:** React Router v7

### Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (Supabase)
- **AI Service:** OpenRouter API
- **Containerization:** Docker
- **ORM:** SQLAlchemy
- **Video Processing:** yt-dlp

### Infrastructure
- **Frontend Hosting:** Vercel
- **Backend Hosting:** Railway
- **Database:** Supabase
- **CI/CD:** GitHub Actions (auto-deploy)

---

## 📁 Project Structure

```
zuno/
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── app/             # Main app components
│   │   ├── components/      # Reusable UI components
│   │   ├── lib/             # Utilities and API client
│   │   └── pages/           # Page components
│   ├── .env.local           # Local environment config
│   ├── .env.production      # Production environment config
│   ├── package.json
│   ├── vite.config.ts
│   └── vercel.json          # Vercel deployment config
│
├── backend/                  # FastAPI backend
│   ├── main.py              # FastAPI application
│   ├── ai_service.py        # AI integration
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Docker configuration
│   ├── docker-compose.yml   # Local development
│   └── .env.example         # Environment template
│
├── .gitignore
└── README.md
```

---

## 🛠️ Local Development Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Docker and Docker Compose
- Git

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/zuno-production.git
cd zuno-production
```

### 2. Backend Setup (Docker)

```bash
cd backend

# Copy environment template
cp .env.example .env

# Edit .env with your credentials:
# - DATABASE_URL (optional for local, uses SQLite by default)
# - SUPABASE_JWT_SECRET
# - OPENROUTER_API_KEY
# - ALLOWED_ORIGINS

# Start Docker backend
docker-compose up
```

Backend will be available at: http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOF
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_API_BASE_URL=http://localhost:8000
EOF

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:5173

---

## 🚢 Deployment

### Frontend (Vercel)

**Option 1: Vercel CLI**
```bash
cd frontend
vercel --prod
```

**Option 2: GitHub Integration**
1. Connect repository to Vercel
2. Set root directory: `frontend`
3. Framework preset: Vite
4. Add environment variables:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
   - `VITE_API_BASE_URL`

### Backend (Railway)

1. Connect repository to Railway
2. Set root directory: `backend`
3. Add environment variables:
   - `DATABASE_URL` (Supabase PostgreSQL)
   - `SUPABASE_JWT_SECRET`
   - `OPENROUTER_API_KEY`
   - `ALLOWED_ORIGINS` (include Vercel URL)

Railway will automatically detect Dockerfile and deploy.

---

## 🔧 Environment Variables

### Frontend (.env.local / Vercel)

```bash
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_API_BASE_URL=http://localhost:8000  # Local
# VITE_API_BASE_URL=https://your-backend.railway.app  # Production
```

### Backend (.env / Railway)

```bash
DATABASE_URL=postgresql://user:password@host:port/db
SUPABASE_JWT_SECRET=your_jwt_secret
OPENROUTER_API_KEY=your_openrouter_key
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173
PORT=8000  # Railway sets this automatically
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Manual Testing
1. Start both frontend and backend
2. Navigate to http://localhost:5173
3. Sign up / Login
4. Complete onboarding
5. Verify daily tasks load
6. Test AI chat functionality

---

## 📚 Documentation

- **Frontend Deployment:** `frontend/VERCEL_DEPLOYMENT.md`
- **Backend Docker:** `backend/DOCKER.md`
- **Environment Setup:** `frontend/ENVIRONMENT_CONFIG.md`
- **Deployment Complete:** `DEPLOYMENT_COMPLETE.md`

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is private and proprietary.

---

## 🔗 Links

- **Production Frontend:** https://zunofrontendf.vercel.app
- **Production Backend:** https://zuno-production-production.up.railway.app
- **Database:** Supabase (managed)

---

## 🆘 Troubleshooting

### CORS Errors
Ensure `ALLOWED_ORIGINS` in Railway includes your Vercel URL.

### Build Failures
```bash
# Frontend
cd frontend
rm -rf node_modules
npm install
npm run build

# Backend
cd backend
docker-compose down
docker-compose up --build
```

### Database Connection Issues
Verify `DATABASE_URL` uses Supabase Connection Pooler (port 6543 for production).

---

## 👥 Team

Built with ❤️ for effective learning

---

**Status:** 🟢 Production Ready
