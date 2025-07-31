"""
Web Scraper using Playwright for AURAX
"""

import asyncio
import logging
import re
from typing import Optional, Dict, Any
from urllib.parse import urlparse
from playwright.async_api import async_playwright, Browser, Page
from pydantic import BaseModel
import trafilatura

logger = logging.getLogger(__name__)


class ScrapedContent(BaseModel):
    """Model for scraped web content"""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]
    success: bool
    error: Optional[str] = None


class WebScraper:
    """
    Web scraper using Playwright for robust web content extraction
    """
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        """
        Initialize the web scraper
        
        Args:
            headless: Run browser in headless mode
            timeout: Page load timeout in milliseconds
        """
        self.headless = headless
        self.timeout = timeout
        self.browser: Optional[Browser] = None
        self._playwright = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def start(self):
        """Start the browser"""
        try:
            self._playwright = await async_playwright().start()
            self.browser = await self._playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            logger.info("Browser started successfully")
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise
    
    async def close(self):
        """Close the browser and cleanup"""
        try:
            if self.browser:
                await self.browser.close()
                logger.info("Browser closed")
            if self._playwright:
                await self._playwright.stop()
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Validate URL format and safety
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if URL is valid and safe
        """
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Basic security checks
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Block potentially dangerous domains
            dangerous_patterns = [
                r'localhost',
                r'127\.0\.0\.1',
                r'0\.0\.0\.0',
                r'192\.168\.',
                r'10\.',
                r'172\.(1[6-9]|2[0-9]|3[0-1])\.'
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, parsed.netloc):
                    logger.warning(f"Blocked potentially dangerous URL: {url}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating URL {url}: {e}")
            return False
    
    async def _extract_content_with_trafilatura(self, html: str, url: str) -> Optional[str]:
        """
        Extract main content using trafilatura
        
        Args:
            html: Raw HTML content
            url: Source URL
            
        Returns:
            Extracted text content or None
        """
        try:
            extracted = trafilatura.extract(
                html,
                url=url,
                include_comments=False,
                include_tables=True,
                include_formatting=False,
                output_format="txt"
            )
            return extracted
        except Exception as e:
            logger.error(f"Error extracting content with trafilatura: {e}")
            return None
    
    async def _extract_page_metadata(self, page: Page) -> Dict[str, Any]:
        """
        Extract metadata from the page
        
        Args:
            page: Playwright page object
            
        Returns:
            Dictionary with page metadata
        """
        metadata = {}
        
        try:
            # Get page title
            title = await page.title()
            metadata['title'] = title
            
            # Get meta description
            description_element = await page.query_selector('meta[name="description"]')
            if description_element:
                description = await description_element.get_attribute('content')
                metadata['description'] = description
            
            # Get meta keywords
            keywords_element = await page.query_selector('meta[name="keywords"]')
            if keywords_element:
                keywords = await keywords_element.get_attribute('content')
                metadata['keywords'] = keywords
            
            # Get language
            html_element = await page.query_selector('html')
            if html_element:
                lang = await html_element.get_attribute('lang')
                metadata['language'] = lang
            
            # Get canonical URL
            canonical_element = await page.query_selector('link[rel="canonical"]')
            if canonical_element:
                canonical = await canonical_element.get_attribute('href')
                metadata['canonical_url'] = canonical
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
        
        return metadata
    
    async def scrape_url(self, url: str) -> ScrapedContent:
        """
        Scrape content from a single URL
        
        Args:
            url: URL to scrape
            
        Returns:
            ScrapedContent object with results
        """
        if not self._is_valid_url(url):
            return ScrapedContent(
                url=url,
                title="",
                content="",
                metadata={},
                success=False,
                error="Invalid or unsafe URL"
            )
        
        if not self.browser:
            return ScrapedContent(
                url=url,
                title="",
                content="",
                metadata={},
                success=False,
                error="Browser not initialized"
            )
        
        page = None
        try:
            logger.info(f"Starting to scrape URL: {url}")
            
            # Create new page
            page = await self.browser.new_page()
            
            # Set user agent
            await page.set_extra_http_headers({
                'User-Agent': 'AURAX-Bot/1.0 (Autonomous Research Assistant)'
            })
            
            # Navigate to URL
            response = await page.goto(url, timeout=self.timeout, wait_until='domcontentloaded')
            
            if not response or response.status >= 400:
                error_msg = f"HTTP {response.status if response else 'No response'}"
                logger.error(f"Failed to load {url}: {error_msg}")
                return ScrapedContent(
                    url=url,
                    title="",
                    content="",
                    metadata={},
                    success=False,
                    error=error_msg
                )
            
            # Wait for any dynamic content
            await page.wait_for_timeout(2000)
            
            # Extract metadata
            metadata = await self._extract_page_metadata(page)
            
            # Get page content
            html_content = await page.content()
            
            # Extract main content using trafilatura
            extracted_content = await self._extract_content_with_trafilatura(html_content, url)
            
            if not extracted_content:
                # Fallback: extract text from body
                body_element = await page.query_selector('body')
                if body_element:
                    extracted_content = await body_element.inner_text()
                else:
                    extracted_content = ""
            
            # Clean up content
            extracted_content = extracted_content.strip()
            
            if not extracted_content:
                return ScrapedContent(
                    url=url,
                    title=metadata.get('title', ''),
                    content="",
                    metadata=metadata,
                    success=False,
                    error="No content extracted from page"
                )
            
            logger.info(f"Successfully scraped {url}: {len(extracted_content)} characters")
            
            return ScrapedContent(
                url=url,
                title=metadata.get('title', ''),
                content=extracted_content,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return ScrapedContent(
                url=url,
                title="",
                content="",
                metadata={},
                success=False,
                error=str(e)
            )
        finally:
            if page:
                try:
                    await page.close()
                except Exception as e:
                    logger.error(f"Error closing page: {e}")


# Global scraper instance (use as context manager)
async def get_scraper() -> WebScraper:
    """Get a configured web scraper instance"""
    return WebScraper(headless=True, timeout=30000)