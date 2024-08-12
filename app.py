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
from models import db

def create_app():
    # intialize the flask application
    app = Flask(__name__)
    app.config.from_object(Config)

    #initialize database and migration
    db.init_app(app)
    migrate = Migrate(app, db)


    # import blue prints
    from routes.user_routes import user_bp


    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/user')



    return app


if __name__ == '__main__':
    app = create_app()
    # Run the Flask application in debug mode
    app.run(debug=True)
