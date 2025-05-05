from app.services.ai_service import AIService
from app.models.company import Company
from typing import Dict, Optional, Tuple, List

class EnrichmentService:
  """Service for company enrichment operations."""
  
  def __init__(self, ai_service=None):
    """Initialize with an AI service or create a new one."""
    self.ai_service = ai_service or AIService()
  
  async def enrich_company(self, company_id: int) -> Tuple[bool, Optional[Dict], str]:
    """
    Enrich a company with AI-generated summary.
    
    Args:
        company_id: Company ID
        
    Returns:
        Tuple of (success, company dict, error message)
    """
    # Get company
    company = Company.query.get(company_id)
    if not company:
      return False, None, "Company not found"
      
    try:
      # Scrape website if available
      website_content = ""
      scrape_error = None
      
      if company.website:
        website_content, scrape_error = await self.ai_service.scrape_website(company.website)
      
      # Handle scraping errors
      if scrape_error:
        # Save error in AI summary
        company.update(ai_summary=f"Company information unavailable, might not be active.")
        return True, company.to_dict(), ""
      
      # Generate AI summary if content was successfully scraped
      if website_content:
        company_data = company.to_dict()
        ai_summary = await self.ai_service.generate_company_summary(company_data, website_content)
        
        # Update company with AI summary
        company.update(ai_summary=ai_summary)
      else:
        # Save generic error if no content
        company.update(ai_summary="Company information unavailable, might not be active")
      
      return True, company.to_dict(), ""
    except Exception as e:
      # Log error and update company with error message
      error_msg = str(e)
      company.update(ai_summary=f"Company information unavailable, might not be active.")
      return False, company.to_dict(), error_msg
      
  async def batch_enrich_companies(self, company_ids: List[int]) -> Tuple[bool, List[Dict], str]:
    """
    Enrich multiple companies with AI-generated summaries.
    
    Args:
        company_ids: List of company IDs
        
    Returns:
        Tuple of (success, list of enriched companies, error message)
    """
    if not company_ids:
      return False, [], "No company IDs provided"
      
    results = []
    errors = []
    
    for company_id in company_ids:
      success, company_data, error = await self.enrich_company(company_id)
      if success:
        results.append(company_data)
      else:
        errors.append(f"Error enriching company {company_id}: {error}")
    
    return len(errors) == 0, results, ", ".join(errors) if errors else "" 