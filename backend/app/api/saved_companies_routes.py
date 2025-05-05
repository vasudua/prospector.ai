from flask import Blueprint, request, jsonify
from app.models.company import Company, SavedCompany
from app import db

bp = Blueprint('saved_companies', __name__, url_prefix='/api/saved-companies')

@bp.route('/', methods=['GET'])
def get_saved_companies():
    try:
        # In a real app, you'd get the user_id from the session/token
        user_id = request.args.get('user_id', 1)  # Default to 1 for demo
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        query = SavedCompany.query.filter_by(user_id=user_id)
        paginated_saved = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'saved_companies': [saved.to_dict() for saved in paginated_saved.items],
            'total': paginated_saved.total,
            'pages': paginated_saved.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def save_company():
    try:
        data = request.json
        company_id = data.get('company_id')
        user_id = data.get('user_id', 1)  # Default to 1 for demo
        notes = data.get('notes', '')
        
        if not company_id:
            return jsonify({'error': 'Company ID is required'}), 400
            
        # Check if company exists
        company = Company.query.get(company_id)
        if not company:
            return jsonify({'error': 'Company not found'}), 404
            
        # Check if already saved
        existing = SavedCompany.query.filter_by(
            company_id=company_id,
            user_id=user_id
        ).first()
        
        if existing:
            return jsonify({'error': 'Company already saved'}), 400
            
        # Create new saved company
        saved_company = SavedCompany(
            company_id=company_id,
            user_id=user_id,
            notes=notes
        )
        
        db.session.add(saved_company)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'saved_company': saved_company.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:saved_id>', methods=['DELETE'])
def delete_saved_company(saved_id):
    try:
        saved_company = SavedCompany.query.get_or_404(saved_id)
        db.session.delete(saved_company)
        db.session.commit()
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:saved_id>', methods=['PATCH'])
def update_saved_company(saved_id):
    try:
        saved_company = SavedCompany.query.get_or_404(saved_id)
        data = request.json
        
        if 'notes' in data:
            saved_company.notes = data['notes']
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'saved_company': saved_company.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 