from flask import Blueprint, request, jsonify
from app.services.company_service import CompanyService
from app.services.ai_service import AIService
from app.utils.helpers import create_response, error_response, parse_request_args, validate_pagination
from app.utils.url_utils import UrlUtils
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
    
    # Get search query
    search_query = request.args.get('q', '')
    
    # If there's a search query, try to generate SQL first
    generated_sql = None
    if search_query:
      # Try to generate SQL from natural language query
      sql_query, error = await ai_service.generate_sql_query(search_query)
      
      if sql_query:  # If SQL was successfully generated
        try:
          # Execute the SQL query
          companies, total, pages, current_page = CompanyService.execute_sql_query(
            sql_query=sql_query,
            page=page,
            per_page=per_page
          )
          
          # Return results with the SQL query
          return create_response({
            'companies': companies,
            'total': total,
            'pages': pages,
            'current_page': current_page,
            'sql_query': sql_query  # Include the generated SQL
          })
        except Exception as e:
          # If SQL execution fails, fall back to standard search
          print(f"SQL execution failed: {str(e)}, falling back to standard search")
          # Continue to standard search below
      else:
        # If SQL generation failed, continue with AI filters
        print(f"SQL generation failed: {error}, falling back to standard search")
    
    # Fallback to standard search with AI filters
    ai_filters = None
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
      return error_response("Company not found", status=404)
      
    return create_response({'company': company.to_dict()})
  except Exception as e:
    return error_response(f"Error retrieving company: {str(e)}") 