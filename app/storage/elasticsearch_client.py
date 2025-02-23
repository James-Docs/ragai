from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionTimeout
from datetime import datetime
from typing import Dict, List
from app.config import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, ELASTICSEARCH_INDEX
import time

class ElasticsearchClient:
    def __init__(self):
        self.es = Elasticsearch(
            "http://localhost:9200",
            timeout=30,  # Increase timeout to 30 seconds
            max_retries=3,  # Add retries
            retry_on_timeout=True  # Retry on timeout
        )
        self.index_name = "documents"
        self.create_index_if_not_exists()  # Call this in init
    
    def create_index_if_not_exists(self):
        try:
            # Check if index exists
            if not self.es.indices.exists(index=self.index_name):
                # Create index with settings
                index_settings = {
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0
                    },
                    "mappings": {
                        "properties": {
                            "content": {"type": "text"},
                            "metadata": {"type": "object"},
                            "embedding_id": {"type": "integer"}
                        }
                    }
                }
                
                # Create the index
                response = self.es.indices.create(
                    index=self.index_name,
                    body=index_settings
                )
                print(f"Index created successfully: {response}")
            else:
                print(f"Index {self.index_name} already exists")
                
        except Exception as e:
            print(f"Error creating index: {e}")
            raise
    
    def index_document(self, doc_id, content, metadata, embedding_id):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                document = {
                    'content': content,
                    'metadata': metadata,
                    'embedding_id': embedding_id
                }
                response = self.es.index(
                    index=self.index_name,
                    id=doc_id,
                    document=document
                )
                print(f"Document indexed successfully on attempt {attempt + 1}: {response}")
                return response
            except ConnectionTimeout as e:
                if attempt == max_retries - 1:  # Last attempt
                    print(f"Final attempt failed: {e}")
                    raise
                print(f"Timeout on attempt {attempt + 1}, retrying...")
                time.sleep(2)  # Wait 2 seconds before retrying
            except Exception as e:
                print(f"Error indexing document: {e}")
                raise
    
    def search(self, query: str, filter_: Dict = None) -> List[Dict]:
        """Search documents using text query and optional filters."""
        body = {
            'query': {
                'bool': {
                    'must': [
                        {'match': {'content': query}}
                    ]
                }
            }
        }
        
        if filter_:
            body['query']['bool']['filter'] = filter_
        
        results = self.es.search(index=ELASTICSEARCH_INDEX, body=body)
        return results['hits']['hits']
    
    def get_document(self, doc_id: str) -> Dict:
        """Retrieve a document by its ID."""
        return self.es.get(index=ELASTICSEARCH_INDEX, id=doc_id)
    
    def delete_document(self, doc_id: str):
        """Delete a document by its ID."""
        self.es.delete(index=ELASTICSEARCH_INDEX, id=doc_id) 