from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config_object='app.config.DevelopmentConfig'):
  """Create application factory."""
  app = Flask(__name__.split('.')[0])
  app.config.from_object(config_object)
  
  # Initialize extensions with app
  register_extensions(app)
  
  # Register blueprints
  register_blueprints(app)
  
  return app

def register_extensions(app):
  """Register Flask extensions."""
  db.init_app(app)
  migrate.init_app(app, db)
  cors.init_app(
    app,
    origins=app.config.get('CORS_ORIGIN_WHITELIST', '*'),
    supports_credentials=True
  )
  return None

def register_blueprints(app):
  """Register Flask blueprints."""
  from app.api import companies, enrichment, saved
  
  app.register_blueprint(companies.blueprint)
  app.register_blueprint(enrichment.blueprint)
  app.register_blueprint(saved.blueprint)
  
  return None 