
from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import uvicorn
from pydantic import BaseModel
from app.pdf_processor import extract_text_from_pdf
from app.rag_engine import rag_engine
from app.llm_service import llm_service

app = FastAPI(title="Research Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    k: int = 10

class QueryResponse(BaseModel):
    answer: str
    context: List[str]

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = extract_text_from_pdf(content)
        if not text:
            return JSONResponse(status_code=400, content={"message": "No text extracted from PDF"})
        
        # Add to RAG index
        rag_engine.add_document(text)
        
        return {"filename": file.filename, "message": "PDF processed and indexed successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    try:
        context_chunks = rag_engine.retrieve(request.query, k=request.k)
        
        if not context_chunks:
            return QueryResponse(answer="I don't have enough context to answer that based on the uploaded documents.", context=[])
        
        context_str = "\n\n".join(context_chunks)
        print(f"DEBUG: LLM Context Length: {len(context_str)} chars")
        print(f"DEBUG: First 200 chars of context: {context_str[:200]}...")
        answer = llm_service.generate_response(context_str, request.query)
        
        return QueryResponse(answer=answer, context=context_chunks)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.delete("/clear")
async def clear_history():
    rag_engine.clear()
    return {"message": "Document history cleared"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
