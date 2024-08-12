from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import relationship
from . import db
class OrderDishes(db.Model):
    __tablename__ = "order_dishes"

    order_dishes_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, ForeignKey("orders.order_id"), nullable=False)
    dish_id = db.Column(db.Integer, ForeignKey("dishes.dish_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Establish relationships
    order = db.relationship("Order", back_populates="order_dishes")
    dish = db.relationship("Dishes", back_populates="order_dishes")

    # Define a string representation
    def __repr__(self):
        return f"<OrderDishes(order_dishes_id={self.order_dishes_id}, order_id={self.order_id}, dish_id={self.dish_id}, quantity={self.quantity})>"
