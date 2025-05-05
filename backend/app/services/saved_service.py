from typing import Dict, List, Optional, Tuple

from app.models.company import Company, SavedCompany

class SavedCompanyService:
  """Service for saved company-related operations."""
  
  @staticmethod
  def get_saved_companies(
    user_id: int,
    page: int = 1,
    per_page: int = 10
  ) -> Tuple[List[Dict], int, int, int]:
    """
    Get saved companies for a user.
    
    Args:
        user_id: User ID
        page: Page number
        per_page: Items per page
        
    Returns:
        Tuple of (saved companies list, total count, total pages, current page)
    """
    query = SavedCompany.query.filter_by(user_id=user_id)
    paginated_saved = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return (
      [saved.to_dict() for saved in paginated_saved.items],
      paginated_saved.total,
      paginated_saved.pages,
      page
    )
  
  @staticmethod
  def save_company(company_id: int, user_id: int, notes: str = '') -> Tuple[bool, Optional[Dict], str]:
    """
    Save a company for a user.
    
    Args:
        company_id: Company ID
        user_id: User ID
        notes: Optional notes
        
    Returns:
        Tuple of (success, saved company dict, error message)
    """
    # Check if company exists
    company = Company.query.get(company_id)
    if not company:
      return False, None, "Company not found"
      
    # Check if already saved
    existing = SavedCompany.query.filter_by(
      company_id=company_id,
      user_id=user_id
    ).first()
    
    if existing:
      return False, None, "Company already saved"
      
    # Create new saved company
    try:
      saved_company = SavedCompany.create(
        company_id=company_id,
        user_id=user_id,
        notes=notes
      )
      return True, saved_company.to_dict(), ""
    except Exception as e:
      return False, None, str(e)
  
  @staticmethod
  def delete_saved_company(saved_id: int) -> Tuple[bool, str]:
    """
    Delete a saved company.
    
    Args:
        saved_id: Saved company ID
        
    Returns:
        Tuple of (success, error message)
    """
    saved_company = SavedCompany.query.get(saved_id)
    if not saved_company:
      return False, "Saved company not found"
      
    try:
      saved_company.delete()
      return True, ""
    except Exception as e:
      return False, str(e)
  
  @staticmethod
  def update_saved_company(saved_id: int, notes: str) -> Tuple[bool, Optional[Dict], str]:
    """
    Update a saved company.
    
    Args:
        saved_id: Saved company ID
        notes: Notes
        
    Returns:
        Tuple of (success, saved company dict, error message)
    """
    saved_company = SavedCompany.query.get(saved_id)
    if not saved_company:
      return False, None, "Saved company not found"
      
    try:
      saved_company.update(notes=notes)
      return True, saved_company.to_dict(), ""
    except Exception as e:
      return False, None, str(e) 