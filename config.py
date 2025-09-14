import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Handle different database environments
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Production - Use external MySQL database
        # Handle different MySQL URL formats
        if database_url.startswith('mysql://'):
            database_url = database_url.replace('mysql://', 'mysql+pymysql://', 1)
        elif not database_url.startswith('mysql+pymysql://'):
            # If it's a raw connection string, format it properly
            database_url = f'mysql+pymysql://{database_url}'
        
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Development - Use local MySQL or SQLite fallback
        mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
        mysql_user = os.environ.get('MYSQL_USER', 'root')
        mysql_password = os.environ.get('MYSQL_PASSWORD', 'password')
        mysql_database = os.environ.get('MYSQL_DATABASE', 'me_api_playground')
        mysql_port = os.environ.get('MYSQL_PORT', '3306')
        
        if mysql_password:
            SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}'
        else:
            # Fallback to SQLite for local development if no MySQL credentials
            SQLALCHEMY_DATABASE_URI = 'sqlite:///me_api_playground.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'pool_timeout': 20,
        'pool_size': 10,
        'max_overflow': 20
    }
