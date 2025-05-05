from app.services.ai_service import AIService
from app.models.company import Company
from typing import Dict, Optional, Tuple

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
      if company.website:
        website_content = await self.ai_service.scrape_website(company.website)
      
      # Generate AI summary
      company_data = company.to_dict()
      ai_summary = await self.ai_service.generate_company_summary(company_data, website_content)
      
      # Update company with AI summary
      company.update(ai_summary=ai_summary)
      
      return True, company.to_dict(), ""
    except Exception as e:
      return False, None, str(e)
      
  async def batch_enrich_companies(self, company_ids: list) -> Tuple[bool, list, str]:
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