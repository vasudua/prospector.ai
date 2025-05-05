from flask import Blueprint, request, jsonify
from app.models.company import Company
from app import db
from app.services.ai_service import AIService
import asyncio

bp = Blueprint('enrichment', __name__, url_prefix='/api/enrichment')
ai_service = AIService()

@bp.route('/company/<int:company_id>', methods=['POST'])
async def enrich_company(company_id):
  try:
    company = Company.query.get_or_404(company_id)
    
    # Scrape website if available
    website_content = ""
    if company.website:
      website_content = await ai_service.scrape_website(company.website)
    
    # Generate AI summary
    company_data = company.to_dict()
    ai_summary = await ai_service.generate_company_summary(company_data, website_content)
    
    # Update company with AI summary
    company.ai_summary = ai_summary
    db.session.commit()
    
    return jsonify({
      'success': True,
      'company': company.to_dict()
    }), 200
    
  except Exception as e:
    return jsonify({'error': str(e)}), 500

@bp.route('/batch', methods=['POST'])
async def enrich_batch():
  try:
    company_ids = request.json.get('company_ids', [])
    if not company_ids:
      return jsonify({'error': 'No company IDs provided'}), 400
      
    results = []
    for company_id in company_ids:
      try:
        company = Company.query.get(company_id)
        if not company:
          continue
          
        # Scrape website if available
        website_content = ""
        if company.website:
          website_content = await ai_service.scrape_website(company.website)
        
        # Generate AI summary
        company_data = company.to_dict()
        ai_summary = await ai_service.generate_company_summary(company_data, website_content)
        
        # Update company with AI summary
        company.ai_summary = ai_summary
        results.append(company.to_dict())
        
      except Exception as e:
        print(f"Error enriching company {company_id}: {e}")
        continue
    
    db.session.commit()
    
    return jsonify({
      'success': True,
      'enriched_companies': results
    }), 200
    
  except Exception as e:
    return jsonify({'error': str(e)}), 500