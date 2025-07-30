"""
RAG Retriever for AURAX System
"""

from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import logging
from .qdrant_client import qdrant_client

logger = logging.getLogger(__name__)


class AuraxRetriever:
    """
    Retrieval component for AURAX RAG system
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the retriever with embedding model
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        try:
            self.embedding_model = SentenceTransformer(model_name)
            self.model_name = model_name
            logger.info(f"Initialized embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Error initializing embedding model: {e}")
            raise
    
    def _get_query_embedding(self, query_text: str) -> List[float]:
        """
        Convert query text to embedding vector
        
        Args:
            query_text: The input query text
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            embedding = self.embedding_model.encode(query_text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding for query: {e}")
            return []
    
    async def search_relevant_context(
        self, 
        query_text: str, 
        top_k: int = 3,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant context documents based on query
        
        Args:
            query_text: The input query text
            top_k: Number of top similar documents to retrieve
            score_threshold: Minimum similarity score threshold
            
        Returns:
            List of relevant context documents with metadata
        """
        if not query_text.strip():
            logger.warning("Empty query text provided")
            return []
        
        try:
            # Ensure Qdrant collection exists
            collection_ready = await qdrant_client.ensure_collection_exists()
            if not collection_ready:
                logger.error("Qdrant collection not ready")
                return []
            
            # Get query embedding
            query_embedding = self._get_query_embedding(query_text)
            if not query_embedding:
                logger.error("Failed to generate query embedding")
                return []
            
            # Search in Qdrant
            search_results = await qdrant_client.search_vectors(
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=score_threshold
            )
            
            # Format results for RAG usage
            context_docs = []
            for result in search_results:
                context_docs.append({
                    "text": result["text"],
                    "score": result["score"],
                    "metadata": result["payload"]
                })
            
            logger.info(f"Retrieved {len(context_docs)} relevant documents for query")
            return context_docs
            
        except Exception as e:
            logger.error(f"Error in search_relevant_context: {e}")
            return []
    
    async def add_documents_to_knowledge_base(
        self, 
        documents: List[Dict[str, Any]]
    ) -> bool:
        """
        Add documents to the knowledge base
        
        Args:
            documents: List of documents with 'text' and optional metadata
            
        Returns:
            bool: True if documents were added successfully
        """
        try:
            if not documents:
                logger.warning("No documents provided to add")
                return False
            
            # Generate embeddings for all documents
            texts = [doc.get("text", "") for doc in documents]
            embeddings = []
            
            for text in texts:
                if text.strip():
                    embedding = self._get_query_embedding(text)
                    embeddings.append(embedding)
                else:
                    logger.warning("Empty text found in document, skipping")
                    continue
            
            if not embeddings:
                logger.error("No valid embeddings generated")
                return False
            
            # Ensure collection exists
            collection_ready = await qdrant_client.ensure_collection_exists()
            if not collection_ready:
                logger.error("Failed to ensure Qdrant collection exists")
                return False
            
            # Add to Qdrant
            success = await qdrant_client.add_documents(documents, embeddings)
            
            if success:
                logger.info(f"Successfully added {len(documents)} documents to knowledge base")
            else:
                logger.error("Failed to add documents to knowledge base")
            
            return success
            
        except Exception as e:
            logger.error(f"Error adding documents to knowledge base: {e}")
            return False
    
    async def get_knowledge_base_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the current knowledge base
        
        Returns:
            Dictionary with knowledge base statistics
        """
        try:
            collection_info = await qdrant_client.get_collection_info()
            if collection_info:
                collection_info["embedding_model"] = self.model_name
            return collection_info
        except Exception as e:
            logger.error(f"Error getting knowledge base info: {e}")
            return None


# Global retriever instance
retriever = AuraxRetriever()