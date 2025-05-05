# Company Search Backend

A Flask-based backend service for company search, enrichment, and CRM functionality.

## Features

- Company search with filtering and pagination
- AI-powered company enrichment
- Saved companies management
- Async support for better performance

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the backend directory with:
```
DATABASE_URL=postgresql://username:password@localhost:5432/company_db
OPENAI_API_KEY=your_openai_api_key
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

## Running the Application

1. Start the Flask development server:
```bash
flask run
```

The server will start at `http://localhost:5000`

## API Endpoints

### Company Search
- `GET /api/companies/search` - Search companies with filters
- `GET /api/companies/<id>` - Get company details

### Company Enrichment
- `POST /api/enrichment/company/<id>` - Generate AI summary for a company
- `POST /api/enrichment/batch` - Generate AI summaries for multiple companies

### Saved Companies
- `GET /api/saved-companies` - Get saved companies
- `POST /api/saved-companies` - Save a company
- `DELETE /api/saved-companies/<id>` - Remove a saved company
- `PATCH /api/saved-companies/<id>` - Update saved company notes

## Development

- The application uses Flask with SQLAlchemy for database operations
- Async support is implemented using asyncio
- AI services are powered by OpenAI's GPT-3.5
- Database migrations are handled by Flask-Migrate

## Testing

Run tests with:
```bash
pytest
``` 