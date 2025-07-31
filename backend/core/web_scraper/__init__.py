"""
AURAX Web Scraper Module
"""

from .scraper import WebScraper, ScrapedContent
from .processor import ContentProcessor
from .rag_updater import RAGUpdater, scrape_and_update_knowledge_base

__all__ = [
    "WebScraper",
    "ScrapedContent", 
    "ContentProcessor",
    "RAGUpdater",
    "scrape_and_update_knowledge_base"
]