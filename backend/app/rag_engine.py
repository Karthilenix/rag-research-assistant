
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
        self.chunk_overlap = 50

    def split_text(self, text: str) -> List[str]:
        # Better splitting strategy: Respect lines (paragraphs)
        chunks = []
        lines = text.split('\n')
        current_chunk = []
        current_length = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            line_len = len(line)
            
            # If adding this line exceeds chunk size, save current chunk and start new
            if current_length + line_len > self.chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    
                    # Handle overlap by keeping the last 2 lines
                    overlap_k = 2
                    if len(current_chunk) > overlap_k:
                        current_chunk = current_chunk[-overlap_k:]
                    
                    current_length = sum(len(l) for l in current_chunk)
                    
            current_chunk.append(line)
            current_length += line_len
            
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        # Fallback to character split if chunks are too huge or empty (unlikely with this logic but good safety)
        if not chunks and text:
             return [text[i:i+self.chunk_size] for i in range(0, len(text), self.chunk_size)]
             
        return chunks

    def clear(self):
        print("DEBUG: Clearing RAG Engine History")
        self.chunks = []
        self.index = None
        # Reset is important to avoid stale data
        if embedding_model:
             # Just to be safe, no special action needed for model
             pass

    def add_document(self, text: str):
        new_chunks = self.split_text(text)
        print(f"DEBUG: Created {len(new_chunks)} chunks from document.")
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
