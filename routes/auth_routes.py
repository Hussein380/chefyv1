from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from app import db, mail, serializer
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

auth_bp = Blueprint('auth', __name__)

# Serializer to generate and decode tokens for secure password reset links

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



# Route to handle password reset request
@auth_bp.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    # Extract the email address from the request JSON
    data = request.get_json()
    email = data.get('email')

    # Check if a user with the provided email exists
    user = User.query.filter_by(email=email).first()
    if not user:
        # Return error response if the user is not found
        return jsonify({'error': 'User not found'}), 404

    # Generate a secure token for the password reset link
    token = serializer.dumps(email, salt='password-reset-salt')
    # Create a password reset link containing the token
    reset_link = url_for('auth.reset_password', token=token, _external=True)

    # Prepare and send the password reset link via email
    msg = Message('Password Reset Request', recipients=[email])
    msg.body = f'Click the link to reset your password: {reset_link}'
    try:
        mail.send(msg)
    except Exception as e:
        return jsonify({'error': 'Failed to send email'}), 500

    # Return success response indicating that the reset link has been sent
    return jsonify({'message': 'Password reset link sent to your email'}), 200

# Route to handle password reset
@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        # Extract the token, new password, and confirmation from the request JSON
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Check if the new password and confirmation match
        if new_password != confirm_password:
            # Return error response if passwords do not match
            return jsonify({'error': 'Passwords do not match'}), 400

        try:
            # Decode the token to get the email address
            email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
        except Exception:
            # Return error response if the token is invalid or expired
            return jsonify({'error': 'Invalid or expired token'}), 400

        # Find the user associated with the email address
        user = User.query.filter_by(email=email).first()
        if not user:
            # Return error response if the user is not found
            return jsonify({'error': 'User not found'}), 404

        # Update the user's password with the new hashed password
        user.password = generate_password_hash(new_password)
        # Commit the changes to the database
        db.session.commit()

        # Return success response indicating that the password has been reset
        return jsonify({'message': 'Password has been reset successfully'}), 200
    # FOR GET request, render the reset form
    token = request.args.get('token') # extract the token from quesry parameters
    return render_template('reset-password.html', token=token)
