from typing import Dict, List, Optional, Tuple, Any

from sqlalchemy import and_, or_, text, inspect

from app import db
from app.models.company import Company
from app.services.ai_service import AIService

class CompanyService:
  """Service for company-related operations."""
  
  @staticmethod
  async def unified_search(
    page: int = 1,
    per_page: int = 10,
    filters: Dict = None,
    text_query: str = None,
    ai_service: AIService = None
  ) -> Tuple[List[Dict], int, int, int, Optional[str]]:
    """
    Unified search function that handles both text queries and filters.
    
    Args:
        page: Page number
        per_page: Items per page
        filters: Dictionary of filter conditions
        text_query: Natural language query to be converted to SQL
        ai_service: AIService instance for AI operations
        
    Returns:
        Tuple of (companies list, total count, total pages, current page, generated SQL query if any)
    """
    # Initialize generated_sql to None
    generated_sql = None
    
    # If AI service is not provided but needed, create one
    if text_query and not ai_service:
      ai_service = AIService()
    
    # Case 1: We have a text query, try to use AI-generated SQL
    if text_query:
      try:
        # Get conditions from filters
        where_conditions = CompanyService._generate_where_conditions(filters) if filters else {}
        
        # Generate SQL with filters included
        sql_query, error = await ai_service.generate_sql_from_text(text_query, where_conditions)
        if error:
          print(f"Error generating SQL: {error}")
          raise ValueError(f"Error generating SQL: {error}")
        
        # Save the generated SQL for returning
        generated_sql = sql_query
        print(f"Final SQL query: {sql_query}")
        
        # Execute the query
        companies, total, pages, current_page = CompanyService.execute_sql_query(
          sql_query=sql_query,
          page=page,
          per_page=per_page
        )
        
        # Return results with the generated SQL
        return companies, total, pages, current_page, generated_sql
      
      except Exception as e:
        # If all SQL generation approaches fail, fall back to filters
        print(f"All SQL approaches failed: {str(e)}, falling back to filters")
    
    # Case 2: No text query or all SQL approaches failed, use standard filtering (Fallback).
    # Extract filters from the text query using AI and combine them using heuristics.
    ai_filters = None
    
    # If we have a text query but SQL generation failed, try to use it for AI filters
    if text_query and ai_service:
      try:
        ai_filters = await ai_service.enhance_search(text_query)
      except Exception as e:
        print(f"Error enhancing search: {str(e)}")
    
    # Use standard search with filters and AI filters
    companies, total, pages, current_page = CompanyService.search_companies(
      page=page,
      per_page=per_page,
      filters=filters,
      ai_filters=ai_filters
    )
    
    # Return results without a generated SQL query
    return companies, total, pages, current_page, None
  
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
  def _generate_where_conditions(filters: Dict) -> Dict[str, Any]:
    """
    Generate WHERE conditions dictionary from filters.
    
    Args:
        filters: Dictionary of filter conditions
        
    Returns:
        Dictionary of field name to value mappings for WHERE conditions
    """
    where_conditions = {}
    
    # Text search fields
    for field in ['name', 'industry', 'country', 'region', 'size', 'locality']:
      if value := filters.get(field):
        where_conditions[field] = f"%{value}%"
    
    # Numeric range fields
    if founded_from := filters.get('founded_from'):
      where_conditions['founded_from'] = int(founded_from)
    if founded_to := filters.get('founded_to'):
      where_conditions['founded_to'] = int(founded_to)
    
    return where_conditions
  
  @staticmethod
  def _get_company_fields() -> List[str]:
    """
    Get all filterable fields from the Company model.
    
    Returns:
        List of field names from the Company model
    """
    # Use SQLAlchemy's inspect to get model columns
    return [column.name for column in inspect(Company).columns]
  
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
      sql_query = sql_query.replace("```sql", "").replace("```", "").strip(";")
      # Ensure the query has an ORDER BY clause for deterministic results
      if "ORDER BY" not in sql_query.upper():
        # Add ordering by ID as a default if no ordering is specified
        sql_query = f"{sql_query} ORDER BY id"
      
      # Create a text SQL query for counting total results
      count_query = text(f"SELECT COUNT(*) FROM ({sql_query}) as count_query")
      count_result = db.session.execute(count_query).scalar()
      
      # Calculate pagination
      total_items = count_result
      total_pages = (total_items + per_page - 1) // per_page
      
      # Adjust page number if out of range
      if page > total_pages and total_pages > 0:
        page = total_pages
      
      # Calculate offset for SQL pagination
      offset = (page - 1) * per_page
      
      # Add pagination to the original query
      paginated_sql = f"{sql_query} LIMIT {per_page} OFFSET {offset}"
      paginated_query = text(paginated_sql)
      
      # Execute the paginated query
      result = db.session.execute(paginated_query)
      
      # Convert to list of dicts
      paginated_items = []
      for row in result:
        # Check if row is a SQLAlchemy Company object
        if isinstance(row, Company):
          paginated_items.append(row.to_dict())
        # Check if row is a tuple with a single Company element
        elif isinstance(row, tuple) and len(row) == 1 and isinstance(row[0], Company):
          paginated_items.append(row[0].to_dict())
        # Otherwise, check if row has a _mapping attribute (new SQLAlchemy style)
        elif hasattr(row, '_mapping'):
          paginated_items.append(dict(row._mapping))
        # Fallback for older SQLAlchemy versions
        else:
          try:
            # Try to convert row to dict
            paginated_items.append(dict(row))
          except Exception:
            # If that fails, process individual fields
            item = {}
            for idx, column in enumerate(result.keys()):
              item[column] = row[idx]
            paginated_items.append(item)
      
      return paginated_items, total_items, total_pages, page
    except Exception as e:
      # Re-raise the exception with more context
      raise ValueError(f"Error executing SQL query: {str(e)}") 