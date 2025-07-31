"""
Content Processor for AURAX Web Scraper
"""

import re
import logging
from typing import List, Dict, Any, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ProcessedChunk(BaseModel):
    """Model for processed content chunk"""
    text: str
    source_url: str
    title: str
    chunk_index: int
    metadata: Dict[str, Any]


class ContentProcessor:
    """
    Content processor for web-scraped content
    """
    
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        min_chunk_size: int = 100
    ):
        """
        Initialize the content processor
        
        Args:
            chunk_size: Target size for text chunks (in characters)
            chunk_overlap: Overlap between consecutive chunks
            min_chunk_size: Minimum size for a chunk to be kept
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", "? ", "! ", " ", ""]
        )
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text content
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common web artifacts
        text = re.sub(r'Cookie\s+Policy|Privacy\s+Policy|Terms\s+of\s+Service', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Subscribe\s+to\s+newsletter|Sign\s+up\s+for\s+updates', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Share\s+on\s+social\s+media|Follow\s+us', '', text, flags=re.IGNORECASE)
        
        # Remove navigation artifacts
        text = re.sub(r'Home\s+>\s+|Breadcrumb|Navigation', '', text, flags=re.IGNORECASE)
        
        # Remove excessive punctuation
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[-]{3,}', '---', text)
        
        # Clean up quotes and apostrophes
        text = re.sub(r'[""]', '"', text)
        text = re.sub(r'['']', "'", text)
        
        return text.strip()
    
    def _filter_chunk(self, chunk: str) -> bool:
        """
        Filter out low-quality chunks
        
        Args:
            chunk: Text chunk to evaluate
            
        Returns:
            True if chunk should be kept
        """
        # Remove chunks that are too short
        if len(chunk) < self.min_chunk_size:
            return False
        
        # Remove chunks with too few words
        word_count = len(chunk.split())
        if word_count < 10:
            return False
        
        # Remove chunks that are mostly numbers or special characters
        alphanumeric_ratio = sum(c.isalnum() or c.isspace() for c in chunk) / len(chunk)
        if alphanumeric_ratio < 0.7:
            return False
        
        # Remove chunks that look like navigation menus
        navigation_patterns = [
            r'^(Home|About|Contact|Services|Products|Blog|News)(\s*\|\s*\w+)*$',
            r'^\d+\s*:\s*\d+\s*(AM|PM)?\s*$',
            r'^Copyright\s+©',
            r'^All\s+rights\s+reserved',
        ]
        
        for pattern in navigation_patterns:
            if re.match(pattern, chunk.strip(), flags=re.IGNORECASE):
                return False
        
        # Remove chunks with excessive repetition
        words = chunk.lower().split()
        if len(set(words)) / len(words) < 0.3:  # Less than 30% unique words
            return False
        
        return True
    
    def _enhance_chunk_metadata(
        self, 
        chunk: str, 
        base_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Enhance chunk metadata with content analysis
        
        Args:
            chunk: Text chunk
            base_metadata: Base metadata from scraping
            
        Returns:
            Enhanced metadata dictionary
        """
        metadata = base_metadata.copy()
        
        # Add chunk statistics
        metadata['chunk_length'] = len(chunk)
        metadata['word_count'] = len(chunk.split())
        metadata['sentence_count'] = len(re.findall(r'[.!?]+', chunk))
        
        # Detect potential content type
        if re.search(r'\b(def\s+\w+|class\s+\w+|import\s+\w+|function\s*\()', chunk):
            metadata['content_type'] = 'code'
        elif re.search(r'\b(Step\s+\d+|First|Second|Next|Finally)\b', chunk, flags=re.IGNORECASE):
            metadata['content_type'] = 'tutorial'
        elif re.search(r'\b(Q:|A:|Question|Answer)\b', chunk, flags=re.IGNORECASE):
            metadata['content_type'] = 'qa'
        else:
            metadata['content_type'] = 'general'
        
        # Extract potential topics (simple keyword extraction)
        technical_keywords = re.findall(
            r'\b(API|database|server|client|authentication|security|performance|optimization|algorithm|data|model|framework|library|service|architecture|design|pattern|testing|deployment|development|programming|software|technology|system|network|web|mobile|cloud|docker|kubernetes|python|javascript|react|node|sql|nosql|rest|graphql|microservice|ai|ml|machine learning|artificial intelligence)\b',
            chunk.lower()
        )
        
        if technical_keywords:
            metadata['topics'] = list(set(technical_keywords[:10]))  # Top 10 unique topics
        
        return metadata
    
    def process_content(
        self,
        content: str,
        source_url: str,
        title: str,
        metadata: Dict[str, Any]
    ) -> List[ProcessedChunk]:
        """
        Process scraped content into chunks suitable for RAG
        
        Args:
            content: Raw text content
            source_url: Source URL
            title: Page title
            metadata: Additional metadata
            
        Returns:
            List of processed chunks
        """
        try:
            if not content or not content.strip():
                logger.warning(f"Empty content for URL: {source_url}")
                return []
            
            # Clean the content
            cleaned_content = self._clean_text(content)
            
            if not cleaned_content:
                logger.warning(f"No content remaining after cleaning for URL: {source_url}")
                return []
            
            # Split into chunks
            chunks = self.text_splitter.split_text(cleaned_content)
            
            # Process and filter chunks
            processed_chunks = []
            for i, chunk in enumerate(chunks):
                # Clean individual chunk
                cleaned_chunk = self._clean_text(chunk)
                
                # Filter out low-quality chunks
                if not self._filter_chunk(cleaned_chunk):
                    continue
                
                # Enhance metadata
                enhanced_metadata = self._enhance_chunk_metadata(cleaned_chunk, metadata)
                enhanced_metadata['processing_timestamp'] = metadata.get('scrape_timestamp')
                
                # Create processed chunk
                processed_chunk = ProcessedChunk(
                    text=cleaned_chunk,
                    source_url=source_url,
                    title=title,
                    chunk_index=i,
                    metadata=enhanced_metadata
                )
                
                processed_chunks.append(processed_chunk)
            
            logger.info(f"Processed {len(processed_chunks)} chunks from {source_url}")
            return processed_chunks
            
        except Exception as e:
            logger.error(f"Error processing content from {source_url}: {e}")
            return []
    
    def process_multiple_contents(
        self,
        contents: List[Dict[str, Any]]
    ) -> List[ProcessedChunk]:
        """
        Process multiple scraped contents
        
        Args:
            contents: List of content dictionaries with keys: content, source_url, title, metadata
            
        Returns:
            List of all processed chunks
        """
        all_chunks = []
        
        for content_data in contents:
            try:
                chunks = self.process_content(
                    content=content_data.get('content', ''),
                    source_url=content_data.get('source_url', ''),
                    title=content_data.get('title', ''),
                    metadata=content_data.get('metadata', {})
                )
                all_chunks.extend(chunks)
            except Exception as e:
                logger.error(f"Error processing content: {e}")
                continue
        
        logger.info(f"Processed total of {len(all_chunks)} chunks from {len(contents)} sources")
        return all_chunks


# Global processor instance
content_processor = ContentProcessor()