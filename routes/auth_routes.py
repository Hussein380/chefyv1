from flask import Blueprint, request, jsonify, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.chef import Chef
from app import db, mail, serializer
from flask_login import login_user
from flask_mail import Message
from flask_login import login_required, current_user
from itsdangerous import URLSafeTimedSerializer

auth_bp = Blueprint('auth', __name__)

# Serializer to generate and decode tokens for secure password reset links


# Route to render the signup page
@auth_bp.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')  # Ensure this template exists


# Route to handle sign-up requests
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email').strip()
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    role = data.get('role')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # validate input fields
    if not all([email, password, confirm_password, role]):
        return jsonify({'error': 'All fields are required'}), 400

    # Validate password match
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email.lower()).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    # Create new user
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    # log the user in
    login_user(new_user)

    #  create chef profile if the user is chef
    if role == 'chef':

        new_chef = Chef(chef_id=new_user.id, user_id =new_user.id, username=new_user.email, latitude=latitude, longitude=longitude)
        
        db.session.add(new_chef)
        db.session.commit()
        print("Chef's location in the database", latitude, longitude)
    # store the location in session
    if role == 'consumer':
        session['latitude'] = latitude
        session['longitude'] = longitude
        print("Latitude stored in session:", session['latitude'])
        print("Longitude stored in session:", session['longitude'])

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
        # log the user in
        login_user(user)

        collect_location = False

        if user.role == 'chef':
            chef = Chef.query.filter_by(user_id=user.id).first()
            if chef and (chef.latitude is None or chef.longitude is None):
                collected_location = True
            return jsonify({'redirect_url': url_for('pages.chef_dashboard'),  'collect_location': collect_location})

        elif user.role == 'consumer':
            # consumer provide their location during login
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            # store the consumers location in session if available
            session['latitude'] = latitude
            session[' longitude'] = longitude

            return jsonify({'redirect_url': url_for('pages.cooks'), 'role': 'consumer'})
    return jsonify({'error': 'Invalid email or password'}), 401



# Route to update user's location after login
@auth_bp.route('/update-location', methods=['POST'])
@login_required
def update_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if current_user.role == 'consumer':
        # update the location in session
        session['latitude'] = latitude
        session['longitude'] = longitude
        return jsonify({'message': 'Chef location updated successfully!'}), 200
    elif current_user.role == 'chef':
        # check if loaction has already beeen collected for the chef
        chef = Chef.query.filter_by(user_id=current_user.id).first()
        if chef and (chef.latitude is None or chef.longitude is None):
            # update the location in Chef Model
            chef.latitude = latitude
            chef.longitude = longitude
            db.session.commit()
        else:
             # Chef already has a location, no need to update
             return jsonify({"message": 'Location already set'}), 200
        # optionally, update the user model to 
    return jsonify({'message': 'Location updated successfully'})


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


