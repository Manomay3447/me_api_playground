from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from config import Config
from models import db, Profile, Skill, Project, WorkExperience, Link
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
db.init_app(app)

# Create tables when app starts
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")

# Frontend route
@app.route('/')
def index():
    return render_template('index.html')

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'message': 'Me-API Playground is running!',
        'database': str(app.config['SQLALCHEMY_DATABASE_URI']).split('@')[0] if '@' in str(app.config['SQLALCHEMY_DATABASE_URI']) else 'Connected'
    }), 200

# Profile endpoints
@app.route('/api/profile', methods=['GET'])
def get_profile():
    try:
        profile_id = request.args.get('id', 1, type=int)
        profile = Profile.query.get_or_404(profile_id)
        return jsonify(profile.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['POST'])
def create_profile():
    try:
        data = request.get_json()
        
        profile = Profile(
            name=data.get('name'),
            email=data.get('email'),
            education=data.get('education', '')
        )
        
        db.session.add(profile)
        db.session.flush()  # Get the profile ID
        
        # Add skills
        for skill_data in data.get('skills', []):
            skill = Skill(
                profile_id=profile.id,
                name=skill_data['name'],
                level=skill_data.get('level', 'beginner')
            )
            db.session.add(skill)
        
        # Add projects
        for project_data in data.get('projects', []):
            project = Project(
                profile_id=profile.id,
                title=project_data['title'],
                description=project_data.get('description', ''),
                technologies=json.dumps(project_data.get('technologies', [])),
                github_url=project_data.get('github_url'),
                demo_url=project_data.get('demo_url')
            )
            db.session.add(project)
        
        # Add work experiences
        for work_data in data.get('work', []):
            work = WorkExperience(
                profile_id=profile.id,
                company=work_data['company'],
                position=work_data['position'],
                description=work_data.get('description', ''),
                start_date=datetime.strptime(work_data['start_date'], '%Y-%m-%d').date() if work_data.get('start_date') else None,
                end_date=datetime.strptime(work_data['end_date'], '%Y-%m-%d').date() if work_data.get('end_date') else None,
                is_current=work_data.get('is_current', False)
            )
            db.session.add(work)
        
        # Add links
        links_data = data.get('links', {})
        for link_type, url in links_data.items():
            if url:
                link = Link(
                    profile_id=profile.id,
                    link_type=link_type,
                    url=url
                )
                db.session.add(link)
        
        db.session.commit()
        return jsonify(profile.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile/<int:profile_id>', methods=['PUT'])
def update_profile(profile_id):
    try:
        profile = Profile.query.get_or_404(profile_id)
        data = request.get_json()
        
        profile.name = data.get('name', profile.name)
        profile.email = data.get('email', profile.email)
        profile.education = data.get('education', profile.education)
        
        db.session.commit()
        return jsonify(profile.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Skills endpoints
@app.route('/api/skills', methods=['GET'])
def get_skills():
    try:
        profile_id = request.args.get('profile_id', 1, type=int)
        skills = Skill.query.filter_by(profile_id=profile_id).all()
        return jsonify([skill.to_dict() for skill in skills]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Projects endpoints
@app.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        profile_id = request.args.get('profile_id', 1, type=int)
        skill = request.args.get('skill')
        
        query = Project.query.filter_by(profile_id=profile_id)
        
        if skill:
            # Filter projects by skill/technology
            query = query.filter(Project.technologies.contains(f'"{skill}"'))
        
        projects = query.all()
        return jsonify([project.to_dict() for project in projects]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Search endpoint
@app.route('/api/search', methods=['GET'])
def search():
    try:
        query = request.args.get('q', '')
        profile_id = request.args.get('profile_id', 1, type=int)
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        results = {
            'skills': [],
            'projects': [],
            'work': []
        }
        
        # Search skills
        skills = Skill.query.filter_by(profile_id=profile_id).filter(
            Skill.name.contains(query)
        ).all()
        results['skills'] = [skill.to_dict() for skill in skills]
        
        # Search projects
        projects = Project.query.filter_by(profile_id=profile_id).filter(
            db.or_(
                Project.title.contains(query),
                Project.description.contains(query),
                Project.technologies.contains(query)
            )
        ).all()
        results['projects'] = [project.to_dict() for project in projects]
        
        # Search work experiences
        work_experiences = WorkExperience.query.filter_by(profile_id=profile_id).filter(
            db.or_(
                WorkExperience.company.contains(query),
                WorkExperience.position.contains(query),
                WorkExperience.description.contains(query)
            )
        ).all()
        results['work'] = [work.to_dict() for work in work_experiences]
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
