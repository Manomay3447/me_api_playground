from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    education = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    skills = db.relationship('Skill', backref='profile', lazy=True, cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='profile', lazy=True, cascade='all, delete-orphan')
    work_experiences = db.relationship('WorkExperience', backref='profile', lazy=True, cascade='all, delete-orphan')
    links = db.relationship('Link', backref='profile', lazy=True, cascade='all, delete-orphan')
    def to_dict(self):
        try:
            result = {
                'id': self.id,
                'name': self.name,
                'email': self.email,
                'education': self.education
            }
        
        # Add timestamp fields if they exist
            if hasattr(self, 'created_at') and self.created_at:
                result['created_at'] = self.created_at.isoformat()
            if hasattr(self, 'updated_at') and self.updated_at:
                result['updated_at'] = self.updated_at.isoformat()
        
        # Add related data safely
            try:
                result['skills'] = [skill.to_dict() for skill in self.skills]
            except:
                result['skills'] = []
            
            try:
                result['projects'] = [project.to_dict() for project in self.projects]
            except:
                result['projects'] = []
            
            try:
                result['work'] = [work.to_dict() for work in self.work_experiences]
            except:
                result['work'] = []
            
            try:
                result['links'] = {link.link_type: link.url for link in self.links}
            except:
                result['links'] = {}
        
            return result
        except Exception as e:
        # Fallback to basic dictionary if there are any errors
            return {
                'id': getattr(self, 'id', None),
                'name': getattr(self, 'name', ''),
                'email': getattr(self, 'email', ''),
                'education': getattr(self, 'education', ''),
                'skills': [],
                'projects': [],
                'work': [],
                'links': {}
            }

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'profile_id': self.profile_id
        }

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    technologies = db.Column(db.Text)  # JSON string of technologies used
    github_url = db.Column(db.String(500))
    demo_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'github_url': self.github_url,
            'demo_url': self.demo_url,
            'profile_id': self.profile_id
        }
    
    # Handle technologies JSON field safely
        try:
            if self.technologies:
                result['technologies'] = json.loads(self.technologies)
            else:
                result['technologies'] = []
        except (json.JSONDecodeError, TypeError):
            result['technologies'] = []
    
        return result

class WorkExperience(db.Model):
    __tablename__ = 'work_experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'company': self.company,
            'position': self.position,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current,
            'profile_id': self.profile_id
        }

class Link(db.Model):
    __tablename__ = 'links'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    link_type = db.Column(db.String(50), nullable=False)  # github, linkedin, portfolio
    url = db.Column(db.String(500), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.link_type,
            'url': self.url,
            'profile_id': self.profile_id
        }
