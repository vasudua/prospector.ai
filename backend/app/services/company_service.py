from sqlalchemy import and_, or_
from app.models.company import Company
from typing import Dict, List, Optional, Tuple

class CompanyService:
  """Service for company-related operations."""
  
  @staticmethod
  def search_companies(
    page: int = 1,
    per_page: int = 10,
    filters: Dict = None,
    ai_filters: Dict = None
  ) -> Tuple[List[Dict], int, int, int]:
    """
    Search companies with filters.
    
    Args:
        page: Page number
        per_page: Items per page
        filters: Dictionary of filter conditions
        ai_filters: Dictionary of AI-enhanced filters
        
    Returns:
        Tuple of (companies list, total count, total pages, current page)
    """
    # Start with base query
    query = Company.query
    
    # Apply standard filters
    if filters:
      filter_conditions = []
      
      # Text search fields
      for field in ['name', 'industry', 'country', 'region', 'size', 'locality']:
        if value := filters.get(field):
          filter_conditions.append(getattr(Company, field).ilike(f'%{value}%'))
      
      # Numeric range fields
      if founded_from := filters.get('founded_from'):
        filter_conditions.append(Company.founded >= int(founded_from))
      if founded_to := filters.get('founded_to'):
        filter_conditions.append(Company.founded <= int(founded_to))
          
      if filter_conditions:
        query = query.filter(and_(*filter_conditions))
    
    # Apply AI-enhanced filters
    if ai_filters:
      ai_filter_conditions = []
      
      for field, value in ai_filters.items():
        if hasattr(Company, field):
          ai_filter_conditions.append(getattr(Company, field).ilike(f'%{value}%'))
          
      if ai_filter_conditions:
        query = query.filter(or_(*ai_filter_conditions))
    
    # Execute paginated query
    paginated_companies = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return (
      [company.to_dict() for company in paginated_companies.items],
      paginated_companies.total,
      paginated_companies.pages,
      page
    )
  
  @staticmethod
  def get_company(company_id: int) -> Optional[Dict]:
    """
    Get company by ID.
    
    Args:
        company_id: Company ID
        
    Returns:
        Company dict or None if not found
    """
    company = Company.query.get(company_id)
    return company.to_dict() if company else None 