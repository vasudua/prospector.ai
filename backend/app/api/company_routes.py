from flask import Blueprint, request, jsonify
from app.models.company import Company
from app import db
from sqlalchemy import and_, or_
import asyncio
from app.services.ai_service import AIService

bp = Blueprint('companies', __name__, url_prefix='/api/companies')
ai_service = AIService()

@bp.route('/search', methods=['GET'])
async def search_companies():
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search_query = request.args.get('q', '')
        
        # Build filter conditions
        filters = []
        for field in ['name', 'industry', 'country', 'region', 'size']:
            if value := request.args.get(field):
                filters.append(getattr(Company, field).ilike(f'%{value}%'))
        
        # Handle founded year range
        if founded_from := request.args.get('founded_from'):
            filters.append(Company.founded >= int(founded_from))
        if founded_to := request.args.get('founded_to'):
            filters.append(Company.founded <= int(founded_to))

        # Base query
        query = Company.query

        # Apply filters if any
        if filters:
            query = query.filter(and_(*filters))

        # Handle AI-powered search if search query is provided
        if search_query:
            # Use AI service to enhance search
            enhanced_filters = await ai_service.enhance_search(search_query)
            if enhanced_filters:
                ai_filters = []
                for field, value in enhanced_filters.items():
                    if hasattr(Company, field):
                        ai_filters.append(getattr(Company, field).ilike(f'%{value}%'))
                if ai_filters:
                    query = query.filter(or_(*ai_filters))

        # Execute paginated query
        paginated_companies = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'companies': [company.to_dict() for company in paginated_companies.items],
            'total': paginated_companies.total,
            'pages': paginated_companies.pages,
            'current_page': page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
    try:
        company = Company.query.get_or_404(company_id)
        return jsonify(company.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 