from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

# Route to handle sign-up requests
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    role = data.get('role')

    # validate input fields
    if not all([email, password, confirm_password, role]):
        return jsonify({'error': 'All fields are required'}), 400

    # Validate password match
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    # Create new user
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    # Return success response and redirect based on role
    if role == 'consumer':
        return jsonify({'message': 'User created', 'redirect_url': url_for('pages.cooks')})
    elif role == 'chef':
        return jsonify({'message': 'User created', 'redirect_url': url_for('pages.chef_dashboard')})
    else:
        return jsonify({'error': 'Invalid role selected'}), 400

# Route to handle login requests
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        if user.role == 'chef':
            return jsonify({'redirect_url': url_for('pages.chef_dashboard')})
        elif user.role == 'consumer':
            return jsonify({'redirect_url': url_for('pages.cooks')})
    return jsonify({'error': 'Invalid email or password'}), 401

