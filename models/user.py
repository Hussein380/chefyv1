from sqlalchemy import Column, Integer, String, Enum
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('consumer', 'chef'), nullable=False, default='consumer') # Or use a separate Role table

    # Relationships
    consumer = db.relationship('Consumer', uselist=False, back_populates='user')
    chef = db.relationship('Chef', uselist=False, back_populates='user')


    # password setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # password checker
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
