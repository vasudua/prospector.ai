import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
  """Base configuration."""
  SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change')
  APP_DIR = os.path.abspath(os.path.dirname(__file__))
  PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8080',
  ]
  OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class DevelopmentConfig(Config):
  """Development configuration."""
  ENV = 'development'
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/company_db')

class TestingConfig(Config):
  """Testing configuration."""
  ENV = 'testing'
  TESTING = True
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:postgres@localhost/company_test_db')

class ProductionConfig(Config):
  """Production configuration."""
  ENV = 'production'
  DEBUG = False
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

# Dictionary with different configuration environments
config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig,
  'default': DevelopmentConfig
} 