from flask import Blueprint, request

from app.services.enrichment_service import EnrichmentService
from app.utils.helpers import create_response, error_response

# Initialize blueprint
blueprint = Blueprint('enrichment', __name__, url_prefix='/api/enrichment')
enrichment_service = EnrichmentService()

@blueprint.route('/company/<int:company_id>', methods=['POST'])
async def enrich_company(company_id):
  """Enrich a company with AI-generated summary."""
  try:
    success, company, error = await enrichment_service.enrich_company(company_id)
    
    if not success:
      return error_response(error or "Failed to enrich company", 400)
      
    return create_response({'company': company})
  except Exception as e:
    return error_response(f"Error enriching company: {str(e)}")

@blueprint.route('/batch', methods=['POST'])
async def batch_enrich():
  """Enrich multiple companies with AI-generated summaries."""
  try:
    data = request.get_json()
    company_ids = data.get('company_ids', [])
    
    if not company_ids:
      return error_response("No company IDs provided", 400)
      
    success, enriched_companies, error = await enrichment_service.batch_enrich_companies(company_ids)
    
    if not success and not enriched_companies:
      return error_response(error or "Failed to enrich companies", 400)
      
    return create_response({
      'enriched_companies': enriched_companies,
      'count': len(enriched_companies),
      'errors': error
    })
  except Exception as e:
    return error_response(f"Error in batch enrichment: {str(e)}") 