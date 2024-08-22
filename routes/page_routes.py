from flask import Blueprint, render_template

page_bp = Blueprint('pages', __name__)

   
@page_bp.route('/')
def home():
    return render_template('herosection.html')

@page_bp.route('/contact-us.html')
def contact_us():
    return render_template('contact-us.html')

@page_bp.route('/login.html')
def login():
    return render_template('login.html')

# Route for chef dashboard
@page_bp.route('/chef_dashboard.html')
def chef_dashboard():
    return render_template('chef_dashboard.html')

# Route for cooks page
@page_bp.route('/cooks.html')
def cooks():
    return render_template('cooks.html')

@page_bp.route('/reset-password.html')
def reset_password():
    return render_template('reset-password.html')
@page_bp.route('/signup.html')
def signup():
    return render_template('signup.html')

