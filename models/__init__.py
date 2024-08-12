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
