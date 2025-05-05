from flask import Blueprint, request
from app.services.saved_service import SavedCompanyService
from app.utils.helpers import create_response, error_response, validate_pagination

# Initialize blueprint
blueprint = Blueprint('saved_companies', __name__, url_prefix='/api/saved-companies')

@blueprint.route('/', methods=['GET'])
def get_saved_companies():
  """Get saved companies for a user."""
  try:
    # In a real app, you'd get the user_id from authentication
    user_id = int(request.args.get('user_id', 1))
    
    # Parse pagination
    page, per_page = validate_pagination(
      request.args.get('page'),
      request.args.get('per_page')
    )
    
    # Get saved companies
    saved_companies, total, pages, current_page = SavedCompanyService.get_saved_companies(
      user_id=user_id,
      page=page,
      per_page=per_page
    )
    
    return create_response({
      'saved_companies': saved_companies,
      'total': total,
      'pages': pages,
      'current_page': current_page
    })
  except Exception as e:
    return error_response(f"Error retrieving saved companies: {str(e)}")

@blueprint.route('/', methods=['POST'])
def save_company():
  """Save a company for a user."""
  try:
    data = request.get_json()
    
    # Extract data from request
    company_id = data.get('company_id')
    user_id = data.get('user_id', 1)  # Default for demo
    notes = data.get('notes', '')
    
    if not company_id:
      return error_response("Company ID is required", 400)
    
    # Save company
    success, saved_company, error = SavedCompanyService.save_company(
      company_id=company_id,
      user_id=user_id,
      notes=notes
    )
    
    if not success:
      return error_response(error or "Failed to save company", 400)
      
    return create_response({'saved_company': saved_company}, status_code=201)
  except Exception as e:
    return error_response(f"Error saving company: {str(e)}")

@blueprint.route('/<int:saved_id>', methods=['DELETE'])
def delete_saved_company(saved_id):
  """Delete a saved company."""
  try:
    success, error = SavedCompanyService.delete_saved_company(saved_id)
    
    if not success:
      return error_response(error or f"Failed to delete saved company with ID {saved_id}", 400)
      
    return create_response({'success': True})
  except Exception as e:
    return error_response(f"Error deleting saved company: {str(e)}")

@blueprint.route('/<int:saved_id>', methods=['PATCH'])
def update_saved_company(saved_id):
  """Update a saved company."""
  try:
    data = request.get_json()
    notes = data.get('notes', '')
    
    success, saved_company, error = SavedCompanyService.update_saved_company(
      saved_id=saved_id,
      notes=notes
    )
    
    if not success:
      return error_response(error or f"Failed to update saved company with ID {saved_id}", 400)
      
    return create_response({'saved_company': saved_company})
  except Exception as e:
    return error_response(f"Error updating saved company: {str(e)}") 