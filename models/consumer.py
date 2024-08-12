from . import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Consumer(db.Model):
    __tablename__ = "consumers"

    consumer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = db.relationship('User', back_populates='consumer')
    orders = db.relationship("Order", back_populates="consumer")

    # Define a string representation
    def __repr__(self):
        return f"<Consumer(consumer_id={self.consumer_id}, user_id={self.user_id})>"

