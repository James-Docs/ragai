from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL
import numpy as np

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        return self.model.encode(text)
    
    def generate_embeddings(self, texts: list[str]) -> np.ndarray:
        """Generate embeddings for multiple texts."""
        return self.model.encode(texts) 