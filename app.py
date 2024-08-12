# app.py
'''
Sets up the Flask application (app) and the SQLAlchemy instance (db).
mports the database models to ensure they are registered with SQLAlchemy.
Creates the database tables within an application context using db.create_all()

'''
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# intialize the flask application
app = Flask(__name__)
app.config.from_object(Config)

# intialize SQLALchemy and Flask-Migrate
from models import db, init_db
init_db(app)
migrate = Migrate(app, db)

# Import models to ensure they are registered with SQLAlchemy
from models import User, Consumer, Chef, Dishes, Media, Review, Order, OrderDishes


# import blue prints
from routes.user_routes import user_bp


# Register blueprints
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
