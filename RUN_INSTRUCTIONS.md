# Zuno Application - Run Instructions

This guide explains how to run the Zuno application locally.

## Prerequisites
- Python 3.8+
- Node.js and npm

## 1. Backend Setup and Run
The backend is built with FastAPI.

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the backend server:
    ```bash
    python -m uvicorn main:app --reload
    ```
    The backend will be available at `http://127.0.0.1:8000`.

## 2. Frontend Setup and Run
The frontend is built with Vite and React.

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.

## 3. Docker (Alternative)

For containerized deployment, see [DOCKER.md](backend/DOCKER.md) for comprehensive instructions.

**Quick start with Docker:**
```bash
cd backend
docker-compose up
```

The backend will be available at `http://localhost:8000`.

## 4. General Notes
- Ensure your `.env` and `.env.local` files are correctly configured (they should be already if you are running this from the repository).
- The application uses a local SQLite database (`zuno_v2.db`) by default in the backend.
- For production deployment on Railway, see [backend/DOCKER.md](backend/DOCKER.md).
