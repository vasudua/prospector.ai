import aiohttp
from bs4 import BeautifulSoup
import asyncio
import openai
import os
from typing import Dict, Optional
import json
import httpx

class AIService:
  """Service for AI-related operations."""
  
  def __init__(self, api_key=None):
    """Initialize AI service with API key."""
    self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
    # Create an explicit httpx client without proxies to avoid the error
    http_client = httpx.Client()
    self.client = openai.OpenAI(api_key=self.api_key, http_client=http_client)
    
  async def scrape_website(self, url: str) -> str:
    """Scrape website content from URL."""
    if not url:
      return ""
    
    try:
      async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
          if response.status == 200:
            html = await response.text()
            return self._process_html_content(html)
      return ""
    except Exception as e:
      print(f"Error scraping website: {e}")
      return ""
          
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
    
    return text[:500]  # Return first 500 characters

  async def generate_company_summary(self, company_data: Dict, website_content: str) -> str:
    """Generate company summary using AI."""
    try:
      prompt = self._create_summary_prompt(company_data, website_content)
      
      response = await asyncio.to_thread(
        self.client.chat.completions.create,
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
      )
      
      return response.choices[0].message.content.strip()
    except Exception as e:
      print(f"Error generating summary: {e}")
      return ""
      
  def _create_summary_prompt(self, company_data: Dict, website_content: str) -> str:
    """Create prompt for company summary."""
    return f"""
    Based on the following company information and website content, generate a concise summary:
    
    Company Information:
    - Name: {company_data.get('name')}
    - Industry: {company_data.get('industry')}
    - Location: {company_data.get('locality')}, {company_data.get('region')}, {company_data.get('country')}
    - Founded: {company_data.get('founded')}
    - Size: {company_data.get('size')}
    
    Website Content:
    {website_content}
    
    Please provide a 2-3 sentence summary focusing on what the company does and its key characteristics.
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