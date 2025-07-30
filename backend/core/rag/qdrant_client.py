"""
Qdrant Client for AURAX RAG System
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse
from typing import List, Optional, Dict, Any
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class AuraxQdrantClient:
    """
    Qdrant client wrapper for AURAX RAG operations
    """
    
    def __init__(self):
        """Initialize Qdrant client with settings configuration"""
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection_name = settings.qdrant_collection_name
        self.vector_size = settings.qdrant_vector_size
        self.distance_metric = self._get_distance_metric()
    
    def _get_distance_metric(self) -> Distance:
        """Convert string distance metric to Qdrant Distance enum"""
        distance_map = {
            "Cosine": Distance.COSINE,
            "Euclidean": Distance.EUCLID,
            "Dot": Distance.DOT
        }
        return distance_map.get(settings.qdrant_distance_metric, Distance.COSINE)
    
    async def ensure_collection_exists(self) -> bool:
        """
        Ensure the collection exists, create if it doesn't
        
        Returns:
            bool: True if collection exists or was created successfully
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(
                col.name == self.collection_name 
                for col in collections.collections
            )
            
            if not collection_exists:
                logger.info(f"Creating collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=self.distance_metric
                    )
                )
                logger.info(f"Collection {self.collection_name} created successfully")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
            
            return True
            
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            return False
    
    async def search_vectors(
        self, 
        query_vector: List[float], 
        limit: int = 3,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the collection
        
        Args:
            query_vector: The query vector to search for
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score threshold
            
        Returns:
            List of search results with payload and scores
        """
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                with_payload=True
            )
            
            results = []
            for result in search_results:
                results.append({
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload or {},
                    "text": result.payload.get("text", "") if result.payload else ""
                })
            
            logger.info(f"Found {len(results)} similar documents")
            return results
            
        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            return []
    
    async def add_documents(
        self, 
        documents: List[Dict[str, Any]], 
        vectors: List[List[float]]
    ) -> bool:
        """
        Add documents with their vectors to the collection
        
        Args:
            documents: List of document payloads
            vectors: List of corresponding vectors
            
        Returns:
            bool: True if documents were added successfully
        """
        try:
            points = [
                PointStruct(
                    id=i,
                    vector=vector,
                    payload=doc
                )
                for i, (doc, vector) in enumerate(zip(documents, vectors))
            ]
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Added {len(documents)} documents to collection")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False
    
    async def get_collection_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the collection
        
        Returns:
            Dictionary with collection information or None if error
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": info.config.name,
                "vector_size": info.config.params.vectors.size,
                "distance": info.config.params.vectors.distance.value,
                "points_count": info.points_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return None


# Global Qdrant client instance
qdrant_client = AuraxQdrantClient()