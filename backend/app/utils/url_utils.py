import re
import validators
from typing import Tuple, Optional
from urllib.parse import urlparse, urljoin, ParseResult

class UrlUtils:
    """Utility class for URL operations."""
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate if a string is a valid URL.
        
        Args:
            url: URL string to validate
            
        Returns:
            True if valid URL, False otherwise
        """
        if not url:
            return False
            
        # Clean up URL
        url = url.strip()
        
        # Add https:// if no scheme provided
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
            
        # Use validators library
        return validators.url(url)
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalize URL by adding scheme if missing and standardizing format.
        
        Args:
            url: URL to normalize
            
        Returns:
            Normalized URL
        """
        if not url:
            return ""
            
        # Clean up URL
        url = url.strip()
        
        # Add https:// if no scheme provided
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
            
        # Parse URL
        parsed = urlparse(url)
        
        # Remove trailing slash if present
        path = parsed.path
        if path.endswith('/') and path != '/':
            path = path[:-1]
            
        # Reconstruct URL
        normalized = ParseResult(
            scheme=parsed.scheme,
            netloc=parsed.netloc.lower(),
            path=path,
            params=parsed.params,
            query=parsed.query,
            fragment=''  # Remove fragments (not relevant for company identification)
        )
        
        return normalized.geturl()
    
    @staticmethod
    def extract_domain(url: str) -> str:
        """
        Extract domain from URL.
        
        Args:
            url: URL to extract domain from
            
        Returns:
            Domain name
        """
        if not url:
            return ""
            
        # Normalize URL first
        url = UrlUtils.normalize_url(url)
        
        # Parse URL
        parsed = urlparse(url)
        
        # Extract domain
        domain = parsed.netloc
        
        # Remove www. if present
        if domain.startswith('www.'):
            domain = domain[4:]
            
        return domain
    
    @staticmethod
    def is_same_domain(url1: str, url2: str) -> bool:
        """
        Check if two URLs belong to the same domain.
        
        Args:
            url1: First URL
            url2: Second URL
            
        Returns:
            True if same domain, False otherwise
        """
        domain1 = UrlUtils.extract_domain(url1)
        domain2 = UrlUtils.extract_domain(url2)
        
        return domain1.lower() == domain2.lower()
    
    @staticmethod
    def get_base_url(url: str) -> str:
        """
        Get base URL (scheme + domain).
        
        Args:
            url: URL to extract base from
            
        Returns:
            Base URL
        """
        if not url:
            return ""
            
        # Normalize URL first
        url = UrlUtils.normalize_url(url)
        
        # Parse URL
        parsed = urlparse(url)
        
        # Reconstruct base URL
        base = ParseResult(
            scheme=parsed.scheme,
            netloc=parsed.netloc,
            path='',
            params='',
            query='',
            fragment=''
        )
        
        return base.geturl()
    
    @staticmethod
    def clean_linkedin_url(url: str) -> str:
        """
        Clean LinkedIn URL to standardized format.
        
        Args:
            url: LinkedIn URL to clean
            
        Returns:
            Cleaned LinkedIn URL
        """
        if not url:
            return ""
            
        # Check if URL is a LinkedIn URL
        if 'linkedin.com' not in url.lower():
            return url
            
        # Normalize URL first
        url = UrlUtils.normalize_url(url)
        
        # Extract company slug
        match = re.search(r'linkedin\.com/company/([^/]+)', url.lower())
        if match:
            company_slug = match.group(1)
            return f'https://www.linkedin.com/company/{company_slug}'
            
        return url 