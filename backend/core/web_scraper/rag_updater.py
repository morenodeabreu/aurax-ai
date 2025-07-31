"""
RAG Updater for AURAX Web Scraper
Integrates web scraping with the RAG knowledge base
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from .scraper import WebScraper, get_scraper
from .processor import ContentProcessor, content_processor
from ..rag import retriever

logger = logging.getLogger(__name__)


class RAGUpdater:
    """
    Coordinates web scraping and RAG knowledge base updates
    """
    
    def __init__(self):
        """Initialize the RAG updater"""
        self.processor = content_processor
        self.retriever = retriever
    
    async def scrape_and_update_knowledge_base(
        self, 
        url: str,
        custom_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Scrape a URL and update the RAG knowledge base
        
        Args:
            url: URL to scrape
            custom_metadata: Additional metadata to include
            
        Returns:
            Dictionary with operation results
        """
        scrape_timestamp = datetime.utcnow().isoformat()
        
        try:
            logger.info(f"Starting scrape and update process for URL: {url}")
            
            # Step 1: Scrape the URL
            async with await get_scraper() as scraper:
                scraped_result = await scraper.scrape_url(url)
            
            if not scraped_result.success:
                return {
                    "success": False,
                    "url": url,
                    "error": f"Scraping failed: {scraped_result.error}",
                    "timestamp": scrape_timestamp
                }
            
            if not scraped_result.content:
                return {
                    "success": False,
                    "url": url,
                    "error": "No content extracted from URL",
                    "timestamp": scrape_timestamp
                }
            
            # Step 2: Process the scraped content
            logger.info(f"Processing scraped content from {url}")
            
            # Prepare metadata
            base_metadata = scraped_result.metadata.copy()
            base_metadata.update({
                "scrape_timestamp": scrape_timestamp,
                "content_length": len(scraped_result.content),
                "scraper_version": "1.0"
            })
            
            if custom_metadata:
                base_metadata.update(custom_metadata)
            
            # Process content into chunks
            processed_chunks = self.processor.process_content(
                content=scraped_result.content,
                source_url=scraped_result.url,
                title=scraped_result.title,
                metadata=base_metadata
            )
            
            if not processed_chunks:
                return {
                    "success": False,
                    "url": url,
                    "error": "No valid chunks produced from content",
                    "timestamp": scrape_timestamp
                }
            
            # Step 3: Prepare documents for RAG
            logger.info(f"Preparing {len(processed_chunks)} chunks for RAG insertion")
            
            documents = []
            for chunk in processed_chunks:
                doc = {
                    "text": chunk.text,
                    "source_url": chunk.source_url,
                    "title": chunk.title,
                    "chunk_index": chunk.chunk_index,
                    **chunk.metadata
                }
                documents.append(doc)
            
            # Step 4: Add to RAG knowledge base
            logger.info(f"Adding {len(documents)} documents to RAG knowledge base")
            
            rag_success = await self.retriever.add_documents_to_knowledge_base(documents)
            
            if not rag_success:
                return {
                    "success": False,
                    "url": url,
                    "error": "Failed to add documents to RAG knowledge base",
                    "timestamp": scrape_timestamp,
                    "chunks_processed": len(processed_chunks)
                }
            
            # Step 5: Return success result
            result = {
                "success": True,
                "url": url,
                "title": scraped_result.title,
                "timestamp": scrape_timestamp,
                "content_length": len(scraped_result.content),
                "chunks_created": len(processed_chunks),
                "chunks_added_to_rag": len(documents),
                "metadata": {
                    "content_type": base_metadata.get("content_type", "unknown"),
                    "language": base_metadata.get("language"),
                    "description": base_metadata.get("description"),
                    "topics": base_metadata.get("topics", [])
                }
            }
            
            logger.info(f"Successfully completed scrape and update for {url}: {len(documents)} chunks added")
            return result
            
        except Exception as e:
            logger.error(f"Error in scrape_and_update_knowledge_base for {url}: {e}")
            return {
                "success": False,
                "url": url,
                "error": f"Internal error: {str(e)}",
                "timestamp": scrape_timestamp
            }
    
    async def scrape_multiple_urls(
        self, 
        urls: List[str],
        custom_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Scrape multiple URLs and update the RAG knowledge base
        
        Args:
            urls: List of URLs to scrape
            custom_metadata: Additional metadata to include for all URLs
            
        Returns:
            Dictionary with batch operation results
        """
        batch_timestamp = datetime.utcnow().isoformat()
        results = []
        total_chunks = 0
        successful_urls = 0
        
        try:
            logger.info(f"Starting batch scrape for {len(urls)} URLs")
            
            for url in urls:
                try:
                    result = await self.scrape_and_update_knowledge_base(url, custom_metadata)
                    results.append(result)
                    
                    if result["success"]:
                        successful_urls += 1
                        total_chunks += result.get("chunks_added_to_rag", 0)
                    
                except Exception as e:
                    logger.error(f"Error processing URL {url}: {e}")
                    results.append({
                        "success": False,
                        "url": url,
                        "error": str(e),
                        "timestamp": batch_timestamp
                    })
            
            return {
                "success": True,
                "batch_timestamp": batch_timestamp,
                "total_urls": len(urls),
                "successful_urls": successful_urls,
                "failed_urls": len(urls) - successful_urls,
                "total_chunks_added": total_chunks,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error in batch scraping: {e}")
            return {
                "success": False,
                "batch_timestamp": batch_timestamp,
                "error": str(e),
                "results": results
            }
    
    async def get_scraping_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about scraped content in the knowledge base
        
        Returns:
            Dictionary with scraping statistics
        """
        try:
            # Get knowledge base info
            kb_info = await self.retriever.get_knowledge_base_info()
            
            if not kb_info:
                return {
                    "success": False,
                    "error": "Could not retrieve knowledge base information"
                }
            
            # Basic statistics from knowledge base
            stats = {
                "success": True,
                "total_documents": kb_info.get("points_count", 0),
                "knowledge_base_name": kb_info.get("name"),
                "vector_size": kb_info.get("vector_size"),
                "distance_metric": kb_info.get("distance")
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting scraping statistics: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Global RAG updater instance
rag_updater = RAGUpdater()


# Convenience function for direct usage
async def scrape_and_update_knowledge_base(
    url: str,
    custom_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Convenience function to scrape a URL and update the knowledge base
    
    Args:
        url: URL to scrape
        custom_metadata: Additional metadata to include
        
    Returns:
        Dictionary with operation results
    """
    return await rag_updater.scrape_and_update_knowledge_base(url, custom_metadata)