# 🚀 prospector.ai 🚀

A web application for advanced search capabilities with a modern tech stack.

## Project Structure

- `frontend/`: Next.js web application with React 19 and Tailwind CSS
- `backend/`: Flask-based API server with SQLAlchemy
- `postgresql/`: PostgreSQL database configuration

## Getting Started

### Prerequisites

- Node.js (latest LTS version)
- Python 3.9+
- PostgreSQL

### Setup

1. Clone this repository
2. Follow setup instructions in the frontend and backend README files

## Development

- Frontend development server: `cd frontend && npm run dev`
- Backend development server: `cd backend && python run.py`
- PostgreSQL: `cd postgresql && docker compose up -d`
- To setup seed data: `cd backend/seeds && python load_sample_data --file "path_to_seed_file"`

## Future Improvements

1. Advanced AI Discovery - A queue based advanced discovery tool to allow users draw detailed insights based on their queries about the data available within the systems. Use a combination of rabbitmq, Celery and PostgreSQL (required database tables too) to build a stateless distributed system for the above.
2. Prompt improvement for all usecases based on any edge cases discovered.
3. Unit tests for the entire codebase.
4. Productionization changes like Dockerfile, Gunicorn integration with the servers to act as a middle ware and spawn more workers to allow for scalability.
5. Makefiles for easy lifecyle management.

