from sqlalchemy import and_, or_, text
from app.models.company import Company
from app.utils.url_utils import UrlUtils
from typing import Dict, List, Optional, Tuple
from flask_sqlalchemy import SQLAlchemy
from app import db

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
  def get_company(company_id: int) -> Optional[Company]:
    """
    Get company by ID.
    
    Args:
        company_id: Company ID
        
    Returns:
        Company object or None if not found
    """
    return Company.query.get(company_id)
    
  @staticmethod
  def execute_sql_query(
    sql_query: str,
    page: int = 1,
    per_page: int = 10
  ) -> Tuple[List[Dict], int, int, int]:
    """
    Execute SQL query and return paginated results.
    
    Args:
        sql_query: SQL query string
        page: Page number
        per_page: Items per page
        
    Returns:
        Tuple of (companies list, total count, total pages, current page)
    """
    try:
      # Create a text SQL query
      query = text(sql_query)
      
      # Execute query to get all results
      result = db.session.execute(query)
      
      # Convert to list of dicts
      all_items = []
      for row in result:
        # Check if row is a SQLAlchemy Company object
        if isinstance(row, Company):
          all_items.append(row.to_dict())
        # Check if row is a tuple with a single Company element
        elif isinstance(row, tuple) and len(row) == 1 and isinstance(row[0], Company):
          all_items.append(row[0].to_dict())
        # Otherwise, check if row has a _mapping attribute (new SQLAlchemy style)
        elif hasattr(row, '_mapping'):
          all_items.append(dict(row._mapping))
        # Fallback for older SQLAlchemy versions
        else:
          try:
            # Try to convert row to dict
            all_items.append(dict(row))
          except Exception:
            # If that fails, process individual fields
            item = {}
            for idx, column in enumerate(result.keys()):
              item[column] = row[idx]
            all_items.append(item)
      
      # Calculate pagination
      total_items = len(all_items)
      total_pages = (total_items + per_page - 1) // per_page
      
      # Adjust page number if out of range
      if page > total_pages and total_pages > 0:
        page = total_pages
      
      # Get paginated items
      start_idx = (page - 1) * per_page
      end_idx = start_idx + per_page
      paginated_items = all_items[start_idx:end_idx]
      
      return paginated_items, total_items, total_pages, page
    except Exception as e:
      # Re-raise the exception with more context
      raise ValueError(f"Error executing SQL query: {str(e)}") 