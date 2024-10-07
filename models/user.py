from sqlalchemy import Column, Integer, String, Enum
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('consumer', 'chef'), nullable=False, default='consumer') # Or use a separate Role table

    # Relationships
    consumer = db.relationship('Consumer', uselist=False, back_populates='user')
    chef = db.relationship('Chef', uselist=False, back_populates='user')

    # Implement methods required by flask login
    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        # add logic to check if account is active
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


    # password setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # password checker
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
