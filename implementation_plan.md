# Implementation Plan - RAG Research Assistant

This document outlines the step-by-step plan to build the Cloud-Based Research Assistant using RAG, based on the provided requirements.

## 1. Project Setup
- [ ] Create `implementation_plan.md` (This file).
- [ ] Initialize git repository (optional but recommended).

## 2. Backend Implementation (FastAPI)
The backend will handle PDF processing, embedding generation, vector storage, and query processing using Google Gemini.

- [ ] **Setup**:
    - Initialize Python environment in `backend/`.
    - Create `requirements.txt` with dependencies: `fastapi`, `uvicorn`, `python-multipart`, `google-generativeai`, `sentence-transformers`, `faiss-cpu`, `pypdf`, `python-dotenv`.
    - Install dependencies.
- [ ] **Core Logic (`backend/app/`)**:
    - Implement `main.py` for FastAPI app entry.
    - Implement `pdf_processor.py` to extract text from PDFs.
    - Implement `rag_engine.py` for chunking, embedding (SentenceTransformer), and FAISS storage.
    - Implement `llm_service.py` to interact with Google Gemini API.
- [ ] **API Endpoints**:
    - `POST /upload`: Upload PDF, process, and index.
    - `POST /query`: Accept question, retrieve context, generate answer.
    - `POST /clear`: Clear index/history.
- [ ] **Environment Variables**:
    - Setup `.env` for `GOOGLE_API_KEY`.

## 3. Frontend Implementation (React + TypeScript)
The frontend will provide a clean, professional interface for uploading and chatting.

- [ ] **Setup**:
    - Initialize React app in `frontend/` using Vite: `npm create vite@latest . -- --template react-ts`.
    - Install dependencies: `axios`, `react-router-dom`, `lucide-react` (icons), `tailwindcss`, `postcss`, `autoprefixer`.
    - Configure Tailwind CSS.
- [ ] **Components**:
    - `Sidebar`: For file upload and list.
    - `ChatArea`: Display messages (User & AI).
    - `MessageBubble`: Individual message component with citation support.
    - `InputArea`: Text input for questions.
- [ ] **State Management**:
    - Manage chat history and upload status.
- [ ] **Integration**:
    - Connect to Backend APIs (`/upload`, `/query`, `/clear`).

## 4. Design & Polish
- [ ] Apply "Soft Blue" (#2563EB) theme.
- [ ] Ensure "Academic/Professional" aesthetics (Inter font, clean spacing).
- [ ] Responsive adjustments.

## 5. Verification
- [ ] Test PDF upload.
- [ ] Test Q&A accuracy.
- [ ] Verify UI responsiveness.
