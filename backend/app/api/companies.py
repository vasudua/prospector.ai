from flask import Blueprint, request

from app.services.ai_service import AIService
from app.services.company_service import CompanyService
from app.utils.helpers import create_response, error_response, parse_request_args, validate_pagination


# Initialize blueprint
blueprint = Blueprint('companies', __name__, url_prefix='/api/companies')
ai_service = AIService()

@blueprint.route('/search', methods=['GET'])
async def search_companies():
  """Search companies with filtering and/or text queries."""
  try:
    # Parse pagination
    page, per_page = validate_pagination(
      request.args.get('page'),
      request.args.get('per_page')
    )
    
    # Parse filters
    filter_fields = ['name', 'industry', 'country', 'region', 'size', 'locality', 'founded_from', 'founded_to']
    filters = parse_request_args(request.args, filter_fields)
    
    # Get search query
    text_query = request.args.get('q', '')
    
    # Use the unified search method
    companies, total, pages, current_page, generated_sql = await CompanyService.unified_search(
      page=page,
      per_page=per_page,
      filters=filters,
      text_query=text_query,
      ai_service=ai_service
    )
    
    # Prepare response
    response_data = {
      'companies': companies,
      'total': total,
      'pages': pages,
      'current_page': current_page
    }
    
    # Include the SQL query if it was generated
    if generated_sql:
      response_data['sql_query'] = generated_sql
      
    return create_response(response_data)
    
  except Exception as e:
    return error_response(f"Error searching companies: {str(e)}")

@blueprint.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
  """Get company by ID."""
  try:
    company = CompanyService.get_company(company_id)
    if not company:
      return error_response("Company not found", status=404)
      
    return create_response({'company': company.to_dict()})
  except Exception as e:
    return error_response(f"Error retrieving company: {str(e)}") 