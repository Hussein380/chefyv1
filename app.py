# app.py
'''
Sets up the Flask application (app) and the SQLAlchemy instance (db).
imports the database models to ensure they are registered with SQLAlchemy.
Creates the database tables within an application context using db.create_all()

'''
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from flask_login import LoginManager
from flask import Flask, render_template
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from models import User
mail = Mail()
serializer = URLSafeTimedSerializer(Config.SECRET_KEY) 

# intiialize flask login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

def create_app():
    # intialize the flask application
    app = Flask(__name__)
    app.config.from_object(Config)

    #initialize database and migration
    db.init_app(app)
    migrate = Migrate(app, db)
    mail.init_app(app)

    # initilize flask-login
    login_manager.init_app(app)

    # import blue prints
    from routes.auth_routes import  auth_bp
    from routes.page_routes import page_bp 
    from routes.chef_route import chef_bp
    from routes.proximity_route import proximity_bp



    # Register blueprinti
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(page_bp)
    app.register_blueprint(chef_bp)
    app.register_blueprint(proximity_bp)



    return app


if __name__ == '__main__':
    app = create_app()
    # Run the Flask application in debug mode
    app.run(debug=True)
