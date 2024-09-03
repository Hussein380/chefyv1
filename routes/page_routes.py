from flask import Blueprint, render_template
from flask_login import login_required, current_user


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
@login_required
def chef_dashboard():
    if current_user.role == 'chef':
        return render_template('chef_dashboard.html')
    else:
        return render_template('cooks.html')


# Route for cooks page
@page_bp.route('/cooks.html')
@login_required
def cooks():
    if current_user.role == 'consumer':
        return render_template('cooks.html')
    else:
        return render_template('chef_dashboard.html')


@page_bp.route('/reset-password')
def reset_password():
    return render_template('reset-password.html')

# route for requesting to reset password
@page_bp.route('/request_password')
def request_password():
    return render_template('request_password.html')

@page_bp.route('/signup.html')
def signup():
    return render_template('signup.html')

