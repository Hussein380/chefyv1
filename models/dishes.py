# dishes.py
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models import db

class Dishes(db.Model):
    __tablename__ = "dishes"

    dish_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dish_name = db.Column(db.String(255), nullable=False)
    dish_image = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    chef_id = db.Column(db.Integer, ForeignKey("chefs.chef_id"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Establish relationships
    chef = db.relationship("Chef", back_populates="dishes")
    order_dishes = db.relationship("OrderDishes", back_populates="dishes")
    # Define a string representation
    def __repr__(self):
        return f"<Dishes(dish_id={self.dish_id}, dish_name={self.dish_name}, price={self.price}, quantity={self.quantity}, chef_id={self.chef_id})>"

