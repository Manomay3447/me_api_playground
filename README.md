# Me-API Playground

A personal API playground built with Flask, MySQL, and vanilla JavaScript that allows you to store and manage your profile information including skills, projects, work experience, and social links.

## My Resume link - https://drive.google.com/file/d/1AdTTIB_egBUaKnuG0zWPMJJF6viEsc5q/view?usp=sharing 

## Features

- **Complete Profile Management**: Store personal information, education, skills, projects, and work experience
- **RESTful API**: Well-structured endpoints for CRUD operations
- **Search Functionality**: Search across all profile data
- **Interactive Frontend**: Modern web interface for testing and viewing data
- **Responsive Design**: Works on desktop and mobile devices
- **API Documentation**: Built-in documentation for all endpoints

## Requirements

- Python 3.7+
- MySQL 5.7+ or 8.0+
- pip (Python package manager)

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd me_api_playground
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   # Create MySQL database
   mysql -u root -p
   > CREATE DATABASE me_api_playground;
   > exit
   
   # Import schema
   mysql -u root -p me_api_playground < database/schema.sql
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run Application**
   ```bash
   python app.py
   ```

5. **Access Application**
   - Web Interface: http://localhost:5000
   - API Health Check: http://localhost:5000/health

## API Endpoints

### Profile Management
- `GET /api/profile` - Get complete profile
- `POST /api/profile` - Create new profile
- `PUT /api/profile/:id` - Update profile

### Skills & Projects
- `GET /api/skills` - Get all skills
- `GET /api/projects` - Get projects (with optional skill filter)
- `GET /api/search` - Search across all data

### System
- `GET /health` - Health check endpoint

## Project Structure

```
me_api_playground/
├── app.py              # Main Flask application
├── models.py           # Database models
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── database/
│   └── schema.sql     # Database schema
├── static/
│   ├── css/
│   │   └── style.css  # Styles
│   └── js/
│       └── app.js     # Frontend JavaScript
└── templates/
    └── index.html     # Frontend HTML
```

## Usage Examples

### Testing API Endpoints

The web interface provides an interactive API testing tool, or you can use curl:

```bash
# Get profile
curl http://localhost:5000/api/profile

# Search for specific skills
curl "http://localhost:5000/api/search?q=python"

# Filter projects by skill
curl "http://localhost:5000/api/projects?skill=python"
```

### Sample Data

The schema.sql file includes sample data to get you started. You can customize this data or add your own through the API endpoints.

## Customization

- **Database**: Modify `models.py` to add new fields or tables
- **API**: Extend `app.py` with new endpoints
- **Frontend**: Update templates and static files for UI changes
- **Styling**: Customize `static/css/style.css` for different themes

## Deployment

For production deployment:

1. Set `FLASK_ENV=production` in your environment
2. Use a production WSGI server like Gunicorn
3. Configure a reverse proxy (nginx)
4. Set up proper database backups
5. Use environment variables for sensitive configuration

## License

This project is open source and available under the MIT License.
