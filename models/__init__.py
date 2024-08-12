from flask_sqlalchemy import SQLAlchemy
# create an instance of SQLALchemy
db = SQLAlchemy()

# Import all model classes
from .user import User
from .consumer import Consumer
from .chef import Chef
from .dishes import Dishes
from .media import Media
from .review import Review
from .order import Order
from .order_dishes import OrderDishes
# Function to initialize the database with the Flask app
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# List of all the models to be used elsewhere in the application
__all__ = ["db", "Chef", "Consumer", "Dishes", "Order", "OrderDishes", "Review"]

