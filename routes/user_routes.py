from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models import db
import jwt
import re
import datetime  # Make sure to import datetime

# Create a blueprint for user-related routes
user_bp = Blueprint('user', __name__)
SECRET_KEY = 'your_secret_key_here'  # Ensure your secret key is defined

# Helper function to validate email format
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Helper function to check password strength
def is_strong_password(password):
    return len(password) >= 6

# Route for user registration
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    # Validate input fields
    if not username or not email or not password or not role:
        return jsonify({"error": "All fields are required"}), 400

    # Validate role
    if role not in ['consumer', 'chef']:
        return jsonify({"error": "Invalid role"}), 400

    # Validate email format
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    # Validate password strength
    if not is_strong_password(password):
        return jsonify({"error": "Password is too weak"}), 400

    # Check if user with the same email or username already exists
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({"error": "User with this email or username already exists"}), 400

    # Hash the password and create a new user
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password, role=role)
    
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Route for user login
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find the user by email
    user = User.query.filter_by(email=email).first()
    
    # Check if the user exists and the password is correct
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Generate a token
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1) # token expires in one hour
        }, SECRET_KEY, algorithm='HS256')

    return jsonify({"token": token}), 200

# Route for fetching a user profile
@user_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    session = db.session
    user = session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"username": user.username, "email": user.email, "role": user.role}), 200

# Route for updating a user profile
@user_bp.route('/profile/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    user.username = data.get('username', user.username)
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

# Route for deleting a user account
@user_bp.route('/profile/<int:user_id>', methods=['DELETE'])
def delete_user_account(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# Route for serving the registration page
@user_bp.route('/register', methods=['GET'])
def register_page():
    return send_from_directory('static', 'signuphtml')
