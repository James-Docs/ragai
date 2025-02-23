import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Storage paths
STORAGE_DIR = BASE_DIR / "storage"
FAISS_INDEX_PATH = STORAGE_DIR / "faiss_index"
DOCUMENT_STORE_PATH = STORAGE_DIR / "documents"

# Create storage directories if they don't exist
STORAGE_DIR.mkdir(exist_ok=True)
DOCUMENT_STORE_PATH.mkdir(exist_ok=True)

# Model configurations
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Elasticsearch configuration
ELASTICSEARCH_HOST = "localhost"
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_INDEX = "documents"

# Redis configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# Flask configuration
UPLOAD_FOLDER = STORAGE_DIR / "uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size 

# Debug settings
DEBUG_MODE = True  # Set to False in production
SHOW_DEBUG_WINDOW = True  # Toggle debug window in UI