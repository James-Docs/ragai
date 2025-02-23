import faiss
import numpy as np
from pathlib import Path
from typing import List, Tuple
from app.config import FAISS_INDEX_PATH

class FAISSClient:
    def __init__(self):
        self.dimension = 384  # Dimension of MiniLM embeddings
        self.index = self._load_or_create_index()
    
    def _load_or_create_index(self) -> faiss.Index:
        """Load existing FAISS index or create a new one."""
        if Path(FAISS_INDEX_PATH).exists():
            return faiss.read_index(str(FAISS_INDEX_PATH))
        
        index = faiss.IndexFlatL2(self.dimension)
        return index
    
    def add_embeddings(self, embeddings: np.ndarray):
        """Add embeddings to the index."""
        self.index.add(embeddings)
        faiss.write_index(self.index, str(FAISS_INDEX_PATH))
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """Search for similar embeddings."""
        return self.index.search(query_embedding.reshape(1, -1), k) 