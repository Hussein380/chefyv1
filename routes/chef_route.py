from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user, logout_user
from models.chef import Chef
from app import db
import os

chef_bp = Blueprint('chef_bp', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@chef_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@chef_bp.route('/api/chef/create_profile', methods=['POST'])
@login_required
def create_profile():
    """ Create a new profile for a chef. """
    username = request.form.get('username')
    bio = request.form.get('bio')
    whatsapp = request.form.get('whatsapp')
    cuisine_types = request.form.get('cuisine_types')  # Get cuisine types
    location_enabled = 'location_enabled' in request.form

    # Check if profile already exists
    if Chef.query.filter_by(user_id=current_user.id).first():
        return jsonify({"error": "Profile already exists"}), 400

    # Create and store the new chef profile
    new_chef = Chef(
        user_id=current_user.id,
        username=username,
        bio=bio,
        whatsapp=whatsapp,
        cuisine_types=cuisine_types,  # Save cuisine types
        location_enabled=location_enabled
    )
    db.session.add(new_chef)
    db.session.commit()

    return jsonify({"success": "Profile created successfully"})

@chef_bp.route('/api/chef/profile', methods=['GET'])
@login_required
def get_profile():
    chef = Chef.query.filter_by(user_id=current_user.id).first()
    if chef:
        default_profile_picture = 'assets/default_profile.png'
        profile_picture = chef.profile_picture if chef.profile_picture else default_profile_picture
        profile_data = {
            "username": chef.username,
            "bio": chef.bio,
            "profile_picture": f'/uploads/{profile_picture}' if chef.profile_picture else f'/static/{profile_picture}',
            "whatsapp": chef.whatsapp,
            "cuisine_types": chef.cuisine_types,  # Include cuisine types
            "location_enabled": chef.location_enabled
        }
        return jsonify(profile_data)
    return jsonify({"error": "Profile not found"}), 404

@chef_bp.route('/api/chef/update-profile', methods=['POST'])
@login_required
def update_profile():
    """ Update the profile information for the logged-in chef. """
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Parse form data
    username = request.form.get('username')
    bio = request.form.get('bio')
    whatsapp = request.form.get('whatsapp')
    cuisine_types = request.form.get('cuisine_types')  # Get cuisine types
    location_enabled = 'location_enabled' in request.form

    # Get the current chef
    chef = Chef.query.filter_by(user_id=current_user.id).first()
    if not chef:
        return jsonify({"error": "Chef not found"}), 404

    # Handle file upload
    profile_picture = request.files.get('profile_picture')
    if profile_picture and allowed_file(profile_picture.filename):
        filename = secure_filename(profile_picture.filename)
        profile_picture_path = os.path.join(UPLOAD_FOLDER, filename)
        profile_picture.save(profile_picture_path)
        chef.profile_picture = filename  # Save the uploaded image filename

    # Update chef information
    chef.username = username
    chef.bio = bio
    chef.whatsapp = whatsapp
    chef.cuisine_types = cuisine_types  # Update cuisine types
    chef.location_enabled = location_enabled
    db.session.commit()

    return jsonify({"success": "Profile updated successfully"})

@chef_bp.route('/api/chef/delete-profile', methods=['DELETE'])
@login_required
def delete_profile():
    """ Delete the profile of the logged-in chef. """
    chef = Chef.query.filter_by(user_id=current_user.id).first()
    if not chef:
        return jsonify({"error": "Chef not found"}), 404

    # Delete the chef profile
    db.session.delete(chef)
    db.session.commit()

    # Log the user out after deleting the profile
    logout_user()

    # Send response with redirect URL to the frontend
    return jsonify({
        "success": "Profile deleted successfully",
        "redirect_url": "/signup"  # Send the redirect URL to the frontend
    })

