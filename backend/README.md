# Backend - Searcher

The backend API server for Searcher built with Flask, SQLAlchemy, and PostgreSQL.

## Technology Stack

- **Framework**: Flask 3.0 (Async)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Database Migrations**: Flask-Migrate
- **Database**: PostgreSQL
- **API Integration**: OpenAI, Beautiful Soup
- **Data Processing**: Pandas, NumPy
- **Testing**: Pytest

## Development

### Prerequisites

- Python 3.9+
- PostgreSQL
- Virtual environment (venv, conda, etc.)

### Installation

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
flask init-db

# Start development server
python run.py
```

## Folder Structure

- `app/`: Main application package
  - `__init__.py`: Application factory
  - `models/`: Database models
  - `routes/`: API routes and endpoints
  - `services/`: Business logic and services
  - `utils/`: Utility functions
- `tests/`: Unit and integration tests
- `seeds/`: Database seed data
- `logs/`: Application logs
- `manage.py`: Command-line management script
- `run.py`: Development server script

## Environment Variables

Create a `.env` file in the root of the backend directory with the following variables:

```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/searcher
OPENAI_API_KEY=your_openai_api_key
```
