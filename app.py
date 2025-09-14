from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from config import Config
from models import db, Profile, Skill, Project, WorkExperience, Link
import json
import os
import logging
import traceback
import sys
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Enhanced logging for production
if not app.debug:
    app.logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

# Initialize database
db.init_app(app)

# Create tables when app starts with detailed error logging
with app.app_context():
    try:
        # Test database connection first
        db.engine.connect()
        app.logger.info("Database connection successful!")
        
        # Create tables
        db.create_all()
        app.logger.info("Database tables created successfully!")
        print("Database tables created successfully!")
        
        # Test if we can query the database
        try:
            profile_count = Profile.query.count()
            app.logger.info(f"Found {profile_count} profiles in database")
        except Exception as query_error:
            app.logger.error(f"Database query test failed: {query_error}")
            
    except Exception as e:
        app.logger.error(f"Database initialization error: {str(e)}")
        app.logger.error(f"Database URI: {str(app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set'))}")
        app.logger.error(f"Full traceback: {traceback.format_exc()}")
        print(f"Error creating database tables: {e}")

# Frontend route
@app.route('/')
def index():
    return render_template('index.html')

# Enhanced health check endpoint
@app.route('/health')
def health():
    try:
        # Test database connection
        db.engine.connect()
        db_status = "Connected"
        
        # Count records in each table
        try:
            profile_count = Profile.query.count()
            skill_count = Skill.query.count()
            project_count = Project.query.count()
            work_count = WorkExperience.query.count()
            link_count = Link.query.count()
            
            db_details = f"Profiles: {profile_count}, Skills: {skill_count}, Projects: {project_count}, Work: {work_count}, Links: {link_count}"
        except Exception as table_error:
            db_details = f"Table query error: {str(table_error)}"
            
    except Exception as db_error:
        db_status = f"Connection failed: {str(db_error)}"
        db_details = "Database unreachable"
    
    return jsonify({
        'status': 'healthy',
        'message': 'Me-API Playground is running!',
        'database_status': db_status,
        'database_details': db_details,
        'database': str(app.config['SQLALCHEMY_DATABASE_URI']).split('@')[0] if '@' in str(app.config['SQLALCHEMY_DATABASE_URI']) else 'Connected'
    }), 200

# Fixed Profile endpoints
@app.route('/api/profile', methods=['GET'])
def get_profile():
    try:
        app.logger.info("Profile GET request received")
        profile_id = request.args.get('id', 1, type=int)
        app.logger.info(f"Looking for profile with ID: {profile_id}")
        
        # Check if database connection is working
        db.engine.connect()
        app.logger.info("Database connection verified")
        
        # Try to get profile
        profile = Profile.query.get(profile_id)
        
        if profile is None:
            app.logger.warning(f"Profile with ID {profile_id} not found, creating default profile")
            # Create a default profile if none exists
            profile = Profile(
                name="Manomay Mali",
                email="manomay2702@gmail.com",
                education="M.Sc. in Computer Science, Savitribai Phule Pune University"
            )
            
            try:
                db.session.add(profile)
                db.session.commit()
                app.logger.info(f"Created default profile with ID: {profile.id}")
                
                # Add some sample skills
                sample_skills = [
                    Skill(profile_id=profile.id, name="C", level="advanced"),
                    Skill(profile_id=profile.id, name="C++", level="intermediate"),
                    Skill(profile_id=profile.id, name="Java", level="intermediate"),
                    Skill(profile_id=profile.id, name="Python", level="advanced"),
                    Skill(profile_id=profile.id, name="JavaScript", level="intermediate"),
                    Skill(profile_id=profile.id, name="MySQL", level="intermediate")
                ]
                
                for skill in sample_skills:
                    db.session.add(skill)
                
                # Add a sample project
                sample_project = Project(
                    profile_id=profile.id,
                    title="Me API Playground",
                    description="A RESTful API for managing personal profiles",
                    technologies=json.dumps(["Python", "Flask", "MySQL"]),
                    github_url="https://github.com/Manomay3447/me-api-playground",
                    demo_url="https://me-api-playground-6824.onrender.com"
                )
                
                db.session.add(sample_project)
                
                # Add sample work experience
                sample_work = WorkExperience(
                    profile_id=profile.id,
                    company="Predusk Technology Pvt. Ltd.",
                    position="Software & AI Developer",
                    description="Developing applications using Python",
                    start_date=datetime.strptime('2023-01-01', '%Y-%m-%d').date(),
                    is_current=True
                )
                
                db.session.add(sample_work)
                
                # Add sample links
                sample_links = [
                    Link(profile_id=profile.id, link_type="github", url="https://github.com/Manomay3447"),
                    Link(profile_id=profile.id, link_type="linkedin", url="https://www.linkedin.com/in/manomay-mali-35ba71251")
                ]
                
                for link in sample_links:
                    db.session.add(link)
                
                db.session.commit()
                app.logger.info("Sample data created successfully")
                
            except Exception as db_error:
                db.session.rollback()
                app.logger.error(f"Error creating sample data: {db_error}")
                return jsonify({
                    'error': 'Database error while creating profile',
                    'message': str(db_error)
                }), 500
        
        # Convert profile to dictionary with error handling
        try:
            app.logger.info(f"Converting profile {profile.id} to dictionary")
            profile_data = profile.to_dict()
            app.logger.info("Profile converted successfully")
            return jsonify(profile_data), 200
            
        except Exception as dict_error:
            app.logger.error(f"Error in to_dict(): {dict_error}")
            # If to_dict() fails, manually create the dictionary
            profile_data = {
                'id': profile.id,
                'name': profile.name,
                'email': profile.email,
                'education': profile.education
            }
            
            # Add timestamp fields if they exist
            if hasattr(profile, 'created_at') and profile.created_at:
                profile_data['created_at'] = profile.created_at.isoformat()
            
            # Get related data safely
            try:
                skills = Skill.query.filter_by(profile_id=profile.id).all()
                profile_data['skills'] = [{'id': s.id, 'name': s.name, 'level': s.level} for s in skills]
            except Exception as skills_error:
                app.logger.error(f"Error getting skills: {skills_error}")
                profile_data['skills'] = []
            
            try:
                projects = Project.query.filter_by(profile_id=profile.id).all()
                profile_data['projects'] = []
                for p in projects:
                    project_dict = {
                        'id': p.id,
                        'title': p.title,
                        'description': p.description,
                        'github_url': p.github_url,
                        'demo_url': p.demo_url
                    }
                    try:
                        project_dict['technologies'] = json.loads(p.technologies) if p.technologies else []
                    except:
                        project_dict['technologies'] = []
                    profile_data['projects'].append(project_dict)
            except Exception as projects_error:
                app.logger.error(f"Error getting projects: {projects_error}")
                profile_data['projects'] = []
            
            try:
                work = WorkExperience.query.filter_by(profile_id=profile.id).all()
                profile_data['work'] = []
                for w in work:
                    work_dict = {
                        'id': w.id,
                        'company': w.company,
                        'position': w.position,
                        'description': w.description,
                        'is_current': w.is_current,
                        'start_date': w.start_date.isoformat() if w.start_date else None,
                        'end_date': w.end_date.isoformat() if w.end_date else None
                    }
                    profile_data['work'].append(work_dict)
            except Exception as work_error:
                app.logger.error(f"Error getting work experience: {work_error}")
                profile_data['work'] = []
            
            try:
                links = Link.query.filter_by(profile_id=profile.id).all()
                profile_data['links'] = {link.link_type: link.url for link in links}
            except Exception as links_error:
                app.logger.error(f"Error getting links: {links_error}")
                profile_data['links'] = {}
            
            return jsonify(profile_data), 200
            
    except Exception as e:
        app.logger.error(f"Profile GET error: {str(e)}")
        app.logger.error(f"Full traceback: {traceback.format_exc()}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'type': type(e).__name__
        }), 500

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

# Debug endpoint to test profile creation
@app.route('/debug/test-profile')
def debug_test_profile():
    try:
        # Check if any profiles exist
        profile_count = Profile.query.count()
        
        if profile_count == 0:
            # Create a test profile
            test_profile = Profile(
                name="Test User",
                email="test@example.com",
                education="Test Education"
            )
            db.session.add(test_profile)
            db.session.commit()
            
            return jsonify({
                'message': 'Test profile created',
                'profile_id': test_profile.id,
                'profile_data': test_profile.to_dict()
            }), 200
        else:
            # Get the first profile
            first_profile = Profile.query.first()
            return jsonify({
                'message': f'Found {profile_count} profiles',
                'first_profile': first_profile.to_dict()
            }), 200
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
