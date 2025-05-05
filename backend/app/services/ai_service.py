import aiohttp
from bs4 import BeautifulSoup
import asyncio
import openai
import os
from typing import Dict, Optional, Tuple, List, Union
import json
import httpx
import validators
from playwright.async_api import async_playwright
import re
from app.utils.url_utils import UrlUtils

class AIService:
  """Service for AI-related operations."""
  
  def __init__(self, api_key=None):
    """Initialize AI service with API key."""
    self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
    # Create an explicit httpx client without proxies to avoid the error
    http_client = httpx.Client()
    self.client = openai.OpenAI(api_key=self.api_key, http_client=http_client)
    
  async def scrape_website(self, url: str) -> Tuple[str, Optional[str]]:
    """
    Scrape website content from URL using Playwright.
    
    Args:
        url: Website URL to scrape
        
    Returns:
        Tuple of (content, error_message)
    """
    if not url:
      return "", "No URL provided"
    
    # Validate URL format using UrlUtils
    if not UrlUtils.validate_url(url):
      return "", "Invalid URL format"
    
    # Normalize URL using UrlUtils
    url = UrlUtils.normalize_url(url)

    try:
      async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
          # Set a reasonable timeout
          await page.goto(url, timeout=15000, wait_until="networkidle")
          
          # Get full HTML content including dynamic elements
          html_content = await page.content()
          
          # Process content
          page_text = self._process_html_content(html_content)
          
          # Check if content suggests this is a company website
          if not self._validate_company_content(page_text):
            await browser.close()
            return "", "Company information unavailable, might not be active"
            
          await browser.close()
          return page_text, None
          
        except Exception as e:
          await browser.close()
          return "", f"Error accessing website: {str(e)}"
          
    except Exception as e:
      return "", f"Error initializing browser: {str(e)}"
    
  def _validate_url(self, url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    return UrlUtils.validate_url(url)
    
  def _validate_company_content(self, content: str) -> bool:
    """
    Check if content appears to be from a company website.
    
    Args:
        content: Website content
        
    Returns:
        True if content seems to be from a company website, False otherwise
    """
    if not content or len(content.strip()) < 50:
      return False
      
    # List of common terms found on company websites
    company_indicators = [
      r'\babout\s+us\b', r'\bour\s+company\b', r'\bour\s+team\b', r'\bour\s+mission\b',
      r'\bcontact\s+us\b', r'\bfounded\s+in\b', r'\bservices\b', r'\bproducts\b',
      r'\bsolutions\b', r'\bindustry\b', r'\bcustomer\b', r'\bclient\b'
    ]
    
    # Check for presence of company indicators
    for indicator in company_indicators:
      if re.search(indicator, content, re.IGNORECASE):
        return True
        
    return False
          
  def _process_html_content(self, html: str) -> str:
    """Process HTML content to extract text."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
      script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Break into lines and remove leading and trailing space
    lines = (line.strip() for line in text.splitlines())
    
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
    # Drop blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    # Return full text for better context
    return text

  async def generate_company_summary(self, company_data: Dict, website_content: str) -> str:
    """Generate company summary using AI."""
    if not website_content:
      return "Company information unavailable, might not be active"
    
    try:
      prompt = self._create_summary_prompt(company_data, website_content)
      
      response = await asyncio.to_thread(
        self.client.chat.completions.create,
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
      )
      
      summary = response.choices[0].message.content.strip()
      
      # Validate that generated summary contains company information
      if self._validate_generated_summary(summary):
        return summary
      else:
        return "Company information unavailable, might not be active"
    except Exception as e:
      print(f"Error generating summary: {e}")
      return "Company information unavailable, might not be active"
      
  def _validate_generated_summary(self, summary: str) -> bool:
    """
    Validate that the generated summary contains useful company information.
    
    Args:
        summary: Generated summary text
        
    Returns:
        True if summary appears valid, False otherwise
    """
    # Check for generic or error-like responses
    generic_patterns = [
      r"could not find", r"no information", r"insufficient data",
      r"not enough context", r"unable to determine", r"not available"
    ]
    
    for pattern in generic_patterns:
      if re.search(pattern, summary, re.IGNORECASE):
        return False
        
    # Check minimum length
    if len(summary.split()) < 10:
      return False
      
    return True
      
  def _create_summary_prompt(self, company_data: Dict, website_content: str) -> str:
    """Create prompt for company summary."""
    return f"""
    Based STRICTLY on the following company information and website content, generate a concise summary.
    Do NOT use any external knowledge not contained in the provided information.
    
    Company Information:
    - Name: {company_data.get('name')}
    - Industry: {company_data.get('industry')}
    - Location: {company_data.get('locality')}, {company_data.get('region')}, {company_data.get('country')}
    - Founded: {company_data.get('founded')}
    - Size: {company_data.get('size')}
    
    Website Content:
    {website_content[:3000]}  # Limit to 3000 chars for context
    
    If you cannot determine what the company does from the provided information, respond with only:
    "Unable to determine company information from the provided content."
    
    Otherwise, please provide a 2-3 sentence summary focusing on what the company does and its key characteristics,
    ONLY using the information provided above.
    """

  async def enhance_search(self, search_query: str) -> Optional[Dict]:
    """Enhance search query using AI to extract structured filters."""
    if not search_query:
      return None
      
    try:
      prompt = self._create_search_enhancement_prompt(search_query)
      
      response = await asyncio.to_thread(
        self.client.chat.completions.create,
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
      )
      
      # Parse the response to extract filters
      try:
        return json.loads(response.choices[0].message.content.strip())
      except:
        return None
    except Exception as e:
      print(f"Error enhancing search: {e}")
      return None
      
  def _create_search_enhancement_prompt(self, search_query: str) -> str:
    """Create prompt for search enhancement."""
    return f"""
    Analyze the following search query and extract relevant filters for company search:
    Query: "{search_query}"
    
    Return a JSON object with any relevant filters you can extract. Possible fields are:
    - industry
    - country
    - region
    - size
    - founded (as a range)
    
    Example response for "Fast growing tech companies in Europe with 100+ employees":
    {{
      "industry": "tech",
      "country": "Europe",
      "size": "100+"
    }}
    """

  async def generate_sql_query(self, search_text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generate a SQL query from natural language search text using AI.
    
    Args:
        search_text: Natural language search text
        
    Returns:
        Tuple of (sql_query, error_message)
    """
    if not search_text:
      return None, "Empty search query"
      
    try:
      prompt = self._create_sql_generation_prompt(search_text)
      
      response = await asyncio.to_thread(
        self.client.chat.completions.create,
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "You are an expert SQL developer who helps convert natural language to SQL queries. Just give me the SQL query, nothing else."},
          {"role": "user", "content": prompt}
        ],
        max_tokens=300
      )
      
      sql_query = response.choices[0].message.content.strip()

      # Remove ```sql and ``` if present
      sql_query = sql_query.replace("```sql", "").replace("```", "")
      
      # Validate SQL query
      is_valid, error = self._validate_sql_query(sql_query)
      if not is_valid:
        return None, error
        
      return sql_query, None
    except Exception as e:
      error_msg = f"Error generating SQL query: {str(e)}"
      print(error_msg)
      return None, error_msg
      
  def _create_sql_generation_prompt(self, search_text: str) -> str:
    """Create prompt for SQL generation."""
    return f"""
    Convert the following natural language query into a SQL query to search a companies database.
    
    Database schema:
    - companies (id, name, website, founded, size, locality, region, country, industry, linkedin_url, ai_summary)
    
    Natural language query: "{search_text}"
    
    Requirements:
    1. Only generate a valid SQL query that can be executed directly
    2. Return only the SQL query and nothing else
    3. Use proper SQL syntax that works with PostgreSQL
    4. For text searches, use ILIKE for case-insensitive matching
    5. If the natural language is ambiguous or cannot be translated to SQL, respond with "INVALID_QUERY"
    6. Use wildcards (%) appropriately for partial matching
    7. Handle numeric comparisons properly (e.g., founded > 2010)
    8. Always return all fields from the companies table
    """
    
  def _validate_sql_query(self, sql_query: str) -> Tuple[bool, Optional[str]]:
    """
    Validate the generated SQL query.
    
    Args:
        sql_query: Generated SQL query
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if query is the error indicator
    if sql_query == "INVALID_QUERY" or "INVALID_QUERY" in sql_query:
      return False, "Could not generate a valid SQL query from the provided search text."
    
    print(f"Generated SQL query: {sql_query}")
      
    # Basic SQL syntax check
    if not sql_query.strip().lower().startswith("select"):
      return False, "Generated query is not a valid SELECT statement."
      
    # Check for dangerous SQL operations
    dangerous_operations = ["drop", "delete", "truncate", "update", "insert", "alter", "create"]
    for op in dangerous_operations:
      if f" {op} " in sql_query.lower():
        return False, f"Generated query contains prohibited '{op}' operation."
        
    # Verify the query only works with expected tables
    allowed_tables = ["companies"]
    table_pattern = r"from\s+(\w+)"
    tables = re.findall(table_pattern, sql_query.lower())
    
    for table in tables:
      if table not in allowed_tables:
        return False, f"Generated query references unauthorized table: {table}"
    
    return True, None 