
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple
import os

# Load model once at startup
# Using a small model for efficiency
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading embedding model: {e}")
    embedding_model = None

class RAGEngine:
    def __init__(self):
        self.chunks = []
        self.index = None
        self.chunk_size = 300
        self.chunk_overlap = 100

    def split_text(self, text: str) -> List[str]:
        # Simple character splitting for demonstration
        # In production, use langchain RecursiveCharacterTextSplitter
        chunks = []
        text_len = len(text)
        start = 0
        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            chunks.append(text[start:end])
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def clear(self):
        self.chunks = []
        self.index = None

    def add_document(self, text: str):
        new_chunks = self.split_text(text)
        if not new_chunks:
            return
            
        embeddings = embedding_model.encode(new_chunks)
        embeddings = np.array(embeddings).astype('float32')

        dimension = embeddings.shape[1]
        
        if self.index is None:
            self.index = faiss.IndexFlatL2(dimension)
            
        self.index.add(embeddings)
        self.chunks.extend(new_chunks)

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        if not self.chunks or self.index is None:
            return []
            
        query_embedding = embedding_model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.chunks):
                chunk = self.chunks[idx]
                results.append(chunk)
                print(f"DEBUG: Retrieved chunk (dist: {distances[0][len(results)-1]}): {chunk[:100]}...")
                
        return results

rag_engine = RAGEngine()
