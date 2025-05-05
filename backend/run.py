#!/usr/bin/env python
from app import create_app, db
import os

app = create_app(os.getenv('FLASK_CONFIG', 'app.config.DevelopmentConfig'))

@app.cli.command('init-db')
def init_db():
  """Initialize the database."""
  db.create_all()
  print('Initialized the database.')

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=app.config['DEBUG'], port=5001) 