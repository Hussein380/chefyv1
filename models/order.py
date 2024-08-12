# order.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import db

class Order(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime(timezone=True), default=func.now())  # Ensures current timestamp
    consumer_id = db.Column(db.Integer, ForeignKey("consumers.consumer_id"))
    chef_id = db.Column(db.Integer, ForeignKey("chefs.chef_id"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Establish relationships
    chef = db.relationship("Chef", back_populates="orders")
    consumer = db.relationship("Consumer", back_populates="orders")
    order_dishes = db.relationship("OrderDishes", back_populates="order")

    # Define a string representation
    def __repr__(self):
        return f"<Order(order_id={self.order_id}, order_date={self.order_date}, consumer_id={self.consumer_id}, chef_id={self.chef_id})>"

