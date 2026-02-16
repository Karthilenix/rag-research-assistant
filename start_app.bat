@echo off
echo Starting Backend...
start "RAG Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload"

echo Starting Frontend...
start "RAG Frontend" cmd /k "cd frontend && npm run dev"

echo Application launched. Access Frontend at http://localhost:5173
pause
