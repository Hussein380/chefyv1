from sqlalchemy import Column, Integer, String, Enum
from models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('consumer', 'chef'), nullable=False)  # Or use a separate Role table

    # Relationships
    consumer = db.relationship('Consumer', uselist=False, back_populates='user')
    chef = db.relationship('Chef', uselist=False, back_populates='user')
