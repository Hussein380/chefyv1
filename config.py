# app/config.py

import os

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'u3p_#)1_w8_%zet^^k*s3$al4v9@qm6qr3jsi)2x_)qn7--m_m')
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://HomeMade:hzg%40746789@localhost/HomeMade')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
