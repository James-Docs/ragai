# Retrieval-Augmented Generation (RAG) Application

## Overview

This project implements a fully local Retrieval-Augmented Generation (RAG) application in Python. The application allows users to upload various document types (text files, PDFs, HTML pages), processes the data into embeddings, and stores it for fast retrieval. Users can ask natural language questions about the uploaded data, and the system retrieves relevant information and generates answers using a pre-trained language model.

## Features

- **Data Upload and Processing**: Users can upload documents, which are then processed to extract text, chunk it into smaller pieces, and generate embeddings.
- **Data Storage**: The application uses FAISS for fast similarity search and Elasticsearch for full-text search and filtering.
- **Query Interface**: Users can ask questions in natural language, and the system retrieves relevant chunks of text and generates answers.
- **Web Interface**: A modern web interface built with Flask allows users to upload documents and ask questions.
- **Persistence**: All data is persisted to disk, ensuring that the application retains its state across restarts.

## Project Structure

The project is organized into several key directories and files:

### Project Structure

rag_app/
├── app/
│ ├── init.py
│ ├── config.py
│ ├── core/
│ │ ├── init.py
│ │ ├── document_processor.py
│ │ ├── embeddings.py
│ │ ├── indexer.py
│ │ └── query_engine.py
│ ├── api/
│ │ ├── init.py
│ │ └── routes.py
│ ├── storage/
│ │ ├── init.py
│ │ ├── elasticsearch_client.py
│ │ ├── faiss_client.py
│ │ └── redis_client.py
│ └── utils/
│ ├── init.py
│ └── text_utils.py
├── requirements.txt
└── run.py

## Main Components

1. **Document Processor** (`app/core/document_processor.py`):
   - Handles reading and extracting text from uploaded documents.
   - Splits the text into smaller chunks for processing.

2. **Embedding Generator** (`app/core/embeddings.py`):
   - Generates embeddings for text chunks using a pre-trained model (e.g., Sentence-BERT).

3. **FAISS Client** (`app/storage/faiss_client.py`):
   - Manages the FAISS index for fast similarity search of embeddings.

4. **Elasticsearch Client** (`app/storage/elasticsearch_client.py`):
   - Handles indexing and searching of documents in Elasticsearch for full-text search capabilities.

5. **Redis Client** (`app/storage/redis_client.py`):
   - Provides caching functionality to speed up frequently accessed data.

6. **Query Engine** (`app/core/query_engine.py`):
   - Processes user queries, retrieves relevant documents from Elasticsearch, and generates answers using the embeddings.

7. **API Routes** (`app/api/routes.py`):
   - Defines the API endpoints for uploading documents and querying the knowledge base.

8. **Configuration** (`app/config.py`):
   - Contains configuration settings for the application, including paths, model settings, and server configurations.

## Interaction Flow

1. **Upload Documents**: Users upload documents through the web interface. The application extracts text, chunks it, and generates embeddings.
2. **Store Data**: The embeddings are stored in a FAISS index, while the raw text and metadata are indexed in Elasticsearch.
3. **Querying**: Users can submit natural language queries. The application retrieves relevant text chunks from Elasticsearch and uses the embeddings to generate answers.
4. **Response**: The generated answers are returned to the user through the web interface.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag_app
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Install and start Elasticsearch and Redis:
   - Follow the official documentation to install and run Elasticsearch and Redis.

4. Run the application:
   ```bash
   python run.py
   ```

5. Access the application at `http://localhost:5000`.

## Usage

- **Upload Documents**: Use the `/upload` endpoint to upload documents.
- **Query the Knowledge Base**: Use the `/query` endpoint to ask questions about the uploaded documents.

## Optional Enhancements

- Implement hybrid search combining keyword-based search in Elasticsearch with vector search in FAISS.
- Add user authentication and error handling.
- Improve the web interface with additional features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Sentence Transformers](https://www.sbert.net/)
- [FAISS](https://faiss.ai/)
- [Elasticsearch](https://www.elastic.co/)
- [Redis](https://redis.io/)


