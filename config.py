# app/config.py

import os
from dotenv import load_dotenv
# load environment variables form .env
load_dotenv()


class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'defualt-secret-key')
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'default_database_url')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
