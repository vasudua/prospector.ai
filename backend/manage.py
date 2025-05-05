#!/usr/bin/env python
import click
from flask.cli import FlaskGroup
from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)
cli = FlaskGroup(create_app=create_app)

@cli.command('init_db')
def init_db():
  """Initialize the database."""
  db.create_all()
  click.echo('Initialized the database.')

if __name__ == '__main__':
  cli() 