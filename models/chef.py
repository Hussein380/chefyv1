from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import db

class Chef(db.Model):
    __tablename__ = 'chefs'

    chef_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(40))
    bio = db.Column(db.String(100))
    profile_picture = db.Column(db.String(255))
    rating = db.Column(db.Float)

    # Assuming a one-to-many relationship between chefs and dishes
    user = db.relationship('User', back_populates='chef')
    dishes = db.relationship('Dishes', back_populates='chef', lazy=True)
    media = db.relationship('Media', back_populates='chef')  # Added
    order = db.relationship('Order', back_populates='chef', lazy=True)

    # One-to-many relationship with Review
    reviews = db.relationship('Review', back_populates='chef', lazy=True)

    def __repr__(self):
        return f"<Chef(chef_id={self.chef_id}, username={self.username}, email={self.email})>"
