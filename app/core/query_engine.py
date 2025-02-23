print("QueryEngine module loaded!")  # This should print when Flask starts

from typing import List, Dict
import numpy as np
from app.core.embeddings import EmbeddingGenerator
from app.storage.faiss_client import FAISSClient
from app.storage.elasticsearch_client import ElasticsearchClient
from app.storage.redis_client import RedisClient
import requests
import json

class QueryEngine:
    def __init__(self):
        print("QueryEngine initialized!")
        self.embedding_generator = EmbeddingGenerator()
        self.faiss_client = FAISSClient()
        self.es_client = ElasticsearchClient()
        self.redis_client = RedisClient()
        self.ollama_url = "http://localhost:11434/api/generate"
        
    def query(self, query_text: str, k: int = 5) -> dict:
        try:
            # Check Redis cache first
            cached_result = self.redis_client.get_cache(query_text)
            print(f"🟡 Backend: Cached result for '{query_text}': {cached_result}")
            if cached_result:
                print("🟡 Backend: Returning cached result from Redis")
                return cached_result
            
            # Generate embedding for query
            print(f"🟡 Backend: Processing query: {query_text}")
            query_embedding = self.embedding_generator.generate_embeddings([query_text])[0]
            
            # Search FAISS
            distances, indices = self.faiss_client.search(query_embedding, k)
            print(f"🟡 Backend: FAISS found {len(indices[0])} similar documents")

            # Get Elasticsearch content
            print(f"🟡 Backend: Retrieving content from Elasticsearch...")
            search_body = {
                "query": {
                    "bool": {
                        "should": [
                            {  # ✅ Retrieve documents that match FAISS results
                                "terms": {
                                    "embedding_id": indices[0].tolist()
                                }
                            },
                            {  # ✅ ALSO retrieve documents that contain the query text
                                "match": {
                                    "content": query_text
                                }
                            }
                        ],
                        "minimum_should_match": 1  # Ensure at least one condition is met
                    }
                },
                "size": 3  # Restrict to top 3 most relevant results
            }

            response = self.es_client.es.search(
                index=self.es_client.index_name,
                body=search_body
            )
            
            hits = response['hits']['hits']
            if hits:
                print(f"🟡 Backend: Found {len(hits)} matching documents in Elasticsearch")
                relevant_content = [hit['_source']['content'] for hit in hits]
                # context = "\n".join(relevant_content)
                context = "\n".join(relevant_content[:2])  # Only keep top 2 most relevant
                
                # Query Ollama
                print(f"🟡 Backend: Querying Ollama...")

                prompt = f"""
                            Based on the following retrieved information:
                {context}

                 Only use this context to answer the question:
                {query_text}
                If the context does not answer the question, say "I don’t know based on the given information."
                """

                # payload = {
                #     "model": "mistral",
                #     "prompt": f"Context: {context}\n\nQuestion: {query_text}\n\nAnswer:",
                #     "stream": False
                # }
                payload = {
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False
                }
                
                ollama_response = requests.post(self.ollama_url, json=payload)
                response_json = ollama_response.json()
                print(f"🟡 Backend: Received response from Ollama")
                
                if 'response' in response_json:
                    print(f"🟡 Backend: Returning response from Ollama")
                    result = {'results': [response_json['response'].strip()]}
                    
                    # Cache the result in Redis
                    self.redis_client.set_cache(query_text, result)
                    print(f"🟡 Backend: Cached result for '{query_text}' in Redis")
                    return result
            else:
                print(f"🟡 Backend: No matching documents found")
                return {
                    'results': ["No relevant information found."],
                }
                
        except Exception as e:
            print(f"🔴 Backend: Error: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise 