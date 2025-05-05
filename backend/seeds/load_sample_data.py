import argparse
import json
import os
import sys

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tqdm import tqdm

from app import create_app, db
from app.models import Company

def load_sample_companies(file_path, limit=1000000):
  """Load sample companies into the database from JSONL file."""
  print(f"Loading up to {limit} sample companies from {file_path}...")
  
  # Load from JSONL file
  try:
    count = 0
    batch = []
    
    with open(file_path, 'r') as f:
      for line in tqdm(f, desc="Loading companies"):
        if count >= limit:
          break
          
        try:
          row = json.loads(line)
          
          company = Company(
            name=row.get('name', ''),
            website=row.get('website', ''),
            founded=int(row.get('founded', 0)) if row.get('founded') and str(row.get('founded')).isdigit() else None,
            size=row.get('size', ''),
            locality=row.get('locality', ''),
            region=row.get('region', ''),
            country=row.get('country', ''),
            industry=row.get('industry', ''),
            linkedin_url=row.get('linkedin_url', '')
          )
          
          batch.append(company)
          count += 1
          
          # Commit in batches
          if count % 1000 == 0:
            print(f"Processed {count} companies...")
            db.session.add_all(batch)
            db.session.commit()
            batch = []
            
        except json.JSONDecodeError:
          print(f"Skipping invalid JSON line: {line[:100]}...")
          continue
    
    # Add remaining batch
    if batch:
      db.session.add_all(batch)
      db.session.commit()
    
    print(f"Successfully loaded {count} companies!")
    
  except Exception as e:
    db.session.rollback()
    print(f"Error loading sample data: {e}")

if __name__ == '__main__':
  app = create_app()
  parser = argparse.ArgumentParser(description='Load sample companies into the database.')
  parser.add_argument('--file', type=str, default='/Users/vasudua/Downloads/free_company_dataset.jsonl.json', help='Path to the JSONL file containing company data.')
  args = parser.parse_args()
  
  with app.app_context():
    # Create tables if they don't exist
    db.create_all()
    
    # Check if we already have data
    if Company.query.count() > 0:
      print("Database already contains companies. Skipping data loading.")
      sys.exit(0)
    
    # Load sample data
    load_sample_companies(args.file) 