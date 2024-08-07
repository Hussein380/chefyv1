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
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models to ensure they are registered with SQLAlchemy
from models import user, consumer, chef, dishes, media, review, order, order_dishes 

# import blue prints
from routes.user_routes import user_bp


# Register blueprints
app.register_blueprint(user_bp, url_prefix='/user')


# Create all tables in the database
with app.app_context():
    db.create_all()

if __name__ = '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
