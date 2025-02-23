import PyPDF2
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Dict
import magic
from app.config import CHUNK_SIZE, CHUNK_OVERLAP
import nltk
nltk.download('punkt_tab')  # Ensure sentence tokenizer is downloaded
from nltk.tokenize import sent_tokenize

class DocumentProcessor:
    def __init__(self, chunk_size=1000, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    @staticmethod
    def read_file(file_path: Path) -> str:
        """Read and extract text from various file types."""
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(str(file_path))
        
        if file_type == "text/plain":
            return DocumentProcessor._read_text_file(file_path)
        elif file_type == "application/pdf":
            return DocumentProcessor._read_pdf_file(file_path)
        elif file_type in ["text/html", "application/html"]:
            return DocumentProcessor._read_html_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    @staticmethod
    def _read_text_file(file_path: Path) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def _read_pdf_file(file_path: Path) -> str:
        text = ""
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    @staticmethod
    def _read_html_file(file_path: Path) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            return soup.get_text()


    def chunk_text(self, text: str) -> list[str]:
        """Break text into chunks using sentence tokenization."""
        print("\nStarting chunking process...")
        print(f"Input text length: {len(text)}")

        try:
            sentences = sent_tokenize(text)  # 🔹 More accurate sentence splitting
            print(f"Split into {len(sentences)} sentences")

            chunks = []
            current_chunk = []
            current_length = 0

            for sentence in sentences:
                sentence_length = len(sentence)

                if current_length + sentence_length > self.chunk_size:
                    # Save current chunk
                    chunk_text = " ".join(current_chunk)
                    print(f"Saving chunk of length {len(chunk_text)}")
                    chunks.append(chunk_text)

                    # Start new chunk with overlap
                    overlap_tokens = current_chunk[-self.overlap:] if self.overlap > 0 else []
                    current_chunk = overlap_tokens + [sentence]
                    current_length = sum(len(t) for t in current_chunk)
                else:
                    current_chunk.append(sentence)
                    current_length += sentence_length

            if current_chunk:
                chunk_text = " ".join(current_chunk)
                print(f"Saving final chunk of length {len(chunk_text)}")
                chunks.append(chunk_text)

            print(f"Chunking complete. Created {len(chunks)} chunks")
            return chunks

        except Exception as e:
            print(f"Error in chunk_text: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise