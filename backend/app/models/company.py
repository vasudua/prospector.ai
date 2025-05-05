from datetime import datetime
from app import db
from sqlalchemy.ext.declarative import declared_attr

class TimestampMixin:
  """Mixin for adding timestamp fields to models."""
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BaseModel(db.Model):
  """Base model class that includes CRUD operations."""
  __abstract__ = True

  @classmethod
  def create(cls, **kwargs):
    """Create a new record and save it to the database."""
    instance = cls(**kwargs)
    return instance.save()

  def update(self, commit=True, **kwargs):
    """Update record."""
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    return self.save() if commit else self

  def save(self, commit=True):
    """Save the record."""
    db.session.add(self)
    if commit:
      db.session.commit()
    return self

  def delete(self, commit=True):
    """Delete the record."""
    db.session.delete(self)
    return commit and db.session.commit()

class Company(BaseModel, TimestampMixin):
  """Company model for storing company information."""
  __tablename__ = 'companies'

  id = db.Column(db.Integer, primary_key=True)
  website = db.Column(db.String(255))
  name = db.Column(db.String(255), nullable=False)
  founded = db.Column(db.Integer)
  size = db.Column(db.String(50))
  locality = db.Column(db.String(255))
  region = db.Column(db.String(255))
  country = db.Column(db.String(255))
  industry = db.Column(db.String(255))
  linkedin_url = db.Column(db.String(255))
  ai_summary = db.Column(db.Text)

  def to_dict(self):
    """Convert company to dictionary."""
    return {
      'id': self.id,
      'website': self.website,
      'name': self.name,
      'founded': self.founded,
      'size': self.size,
      'locality': self.locality,
      'region': self.region,
      'country': self.country,
      'industry': self.industry,
      'linkedin_url': self.linkedin_url,
      'ai_summary': self.ai_summary,
      'created_at': self.created_at.isoformat() if self.created_at else None,
      'updated_at': self.updated_at.isoformat() if self.updated_at else None
    }

  def __repr__(self):
    """String representation of company."""
    return f"<Company(name={self.name}, industry={self.industry})>"

class SavedCompany(BaseModel, TimestampMixin):
  """Model for storing saved company references."""
  __tablename__ = 'saved_companies'

  id = db.Column(db.Integer, primary_key=True)
  company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
  user_id = db.Column(db.Integer, nullable=False)  # In a real app, this would be a foreign key to users table
  notes = db.Column(db.Text)

  # Relationships
  company = db.relationship('Company', backref='saved_instances')

  def to_dict(self):
    """Convert saved company to dictionary."""
    return {
      'id': self.id,
      'company_id': self.company_id,
      'user_id': self.user_id,
      'notes': self.notes,
      'company': self.company.to_dict() if self.company else None,
      'created_at': self.created_at.isoformat() if self.created_at else None,
      'updated_at': self.updated_at.isoformat() if self.updated_at else None
    }

  def __repr__(self):
    """String representation of saved company."""
    return f"<SavedCompany(company_id={self.company_id}, user_id={self.user_id})>" 