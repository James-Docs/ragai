from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfReader
from app.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, SHOW_DEBUG_WINDOW
from app.core.document_processor import DocumentProcessor
from app.core.embeddings import EmbeddingGenerator
from app.core.query_engine import QueryEngine
from app.storage.faiss_client import FAISSClient
from app.storage.elasticsearch_client import ElasticsearchClient

api = Blueprint('api', __name__, url_prefix='/api')
document_processor = DocumentProcessor()
embedding_generator = EmbeddingGenerator()
query_engine = QueryEngine()
faiss_client = FAISSClient()
es_client = ElasticsearchClient()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file_content(file):
    """Read content from either text or PDF files"""
    filename = file.filename.lower()
    if filename.endswith('.pdf'):
        # Handle PDF files
        try:
            pdf_reader = PdfReader(file)
            content = []
            for page in pdf_reader.pages:
                content.append(page.extract_text())
            return '\n'.join(content)
        except Exception as e:
            print(f"PDF reading error: {e}")
            raise
    else:
        # Handle text files
        return file.read().decode('utf-8')

@api.route('/')
def index():
    return render_template('index.html', config={'SHOW_DEBUG_WINDOW': SHOW_DEBUG_WINDOW})

@api.route('/upload', methods=['POST'])
def upload_file():
    print("\n=== Starting Upload Process ===")
    print("Upload endpoint called!")
    
    if 'file' not in request.files:
        print("No file in request")
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        try:
            print(f"\n1. Processing file: {file.filename}")
            
            # Read content with more detailed logging
            print("   Starting content extraction...")
            content = read_file_content(file)
            print(f"2. Content extracted - Length: {len(content)} characters")
            print(f"   First 100 chars: {content[:100]}...")
            
            # Add logging before chunking
            print("\n   Starting text chunking...")
            try:
                chunks = document_processor.chunk_text(content)
                print(f"3. Text chunked into {len(chunks)} parts")
                print(f"   First chunk sample: {chunks[0][:100]}...")
            except Exception as e:
                print(f"!!! Error during chunking: {str(e)}")
                raise
            
            # Add logging before embedding generation
            print("\n   Starting embedding generation...")
            try:
                embeddings = embedding_generator.generate_embeddings(chunks)
                print(f"4. Created {len(embeddings)} embeddings")
            except Exception as e:
                print(f"!!! Error during embedding generation: {str(e)}")
                raise
            
            print("\n5. Starting indexing process...")
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                try:
                    print(f"\n   Processing chunk {i+1}/{len(chunks)}")
                    
                    print("   - Adding to FAISS...")
                    faiss_client.add_embeddings(embedding.reshape(1, -1))
                    print(f"   - Added to FAISS successfully")
                    
                    print("   - Adding to Elasticsearch...")
                    doc_id = f"{file.filename}_{i}"
                    es_client.index_document(
                        doc_id=doc_id,
                        content=chunk,
                        metadata={'source': file.filename},
                        embedding_id=i
                    )
                    print(f"   - Added to Elasticsearch with ID: {doc_id}")
                except Exception as e:
                    print(f"!!! Error processing chunk {i}: {str(e)}")
                    raise
            
            print("\n=== Upload Complete ===")
            return jsonify({'message': f'Document uploaded: {file.filename}'}), 200
            
        except Exception as e:
            print(f"\n!!! Upload error: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

@api.route('/query', methods=['POST'])
def query_documents():
    print("Query endpoint called!")
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        result = query_engine.query(data['query'])
        return jsonify(result), 200
    except Exception as e:
        print(f"Query error: {e}")
        return jsonify({
            'error': str(e),
            'debug_logs': [f"🔴 Backend: Error in query endpoint: {str(e)}"]
        }), 500 