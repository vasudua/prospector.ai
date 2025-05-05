from flask import Blueprint, request
from app.services.company_service import CompanyService
from app.services.ai_service import AIService
from app.utils.helpers import create_response, error_response, parse_request_args, validate_pagination
import asyncio

# Initialize blueprint
blueprint = Blueprint('companies', __name__, url_prefix='/api/companies')
ai_service = AIService()

@blueprint.route('/search', methods=['GET'])
async def search_companies():
  """Search companies with filtering."""
  try:
    # Parse pagination
    page, per_page = validate_pagination(
      request.args.get('page'),
      request.args.get('per_page')
    )
    
    # Parse filters
    filter_fields = ['name', 'industry', 'country', 'region', 'size', 'locality', 'founded_from', 'founded_to']
    filters = parse_request_args(request.args, filter_fields)
    
    # Check for AI-powered search
    ai_filters = None
    search_query = request.args.get('q', '')
    
    if search_query:
      ai_filters = await ai_service.enhance_search(search_query)
    
    # Perform search
    companies, total, pages, current_page = CompanyService.search_companies(
      page=page,
      per_page=per_page,
      filters=filters,
      ai_filters=ai_filters
    )
    
    # Return results
    return create_response({
      'companies': companies,
      'total': total,
      'pages': pages,
      'current_page': current_page
    })
  except Exception as e:
    return error_response(f"Error searching companies: {str(e)}")

@blueprint.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
  """Get company by ID."""
  try:
    company = CompanyService.get_company(company_id)
    
    if not company:
      return error_response(f"Company with ID {company_id} not found", 404)
      
    return create_response({'company': company})
  except Exception as e:
    return error_response(f"Error retrieving company: {str(e)}")

@blueprint.route('/', methods=['GET'])
def index():
  """API index route."""
  return create_response({
    'message': 'Company Search API',
    'endpoints': [
      {'path': '/api/companies/search', 'method': 'GET', 'description': 'Search companies'},
      {'path': '/api/companies/<id>', 'method': 'GET', 'description': 'Get company by ID'}
    ]
  }) 