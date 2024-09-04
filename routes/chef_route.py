from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from models.chef import Chef
from app import db
import os

chef_bp = Blueprint('chef_bp', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@chef_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/uploads', filename)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@chef_bp.route('/api/chef/profile', methods=['GET'])
@login_required
def get_profile():
    """
    Retrieve the profile information for the logged-in chef.
    """
    chef = Chef.query.filter_by(user_id=current_user.id).first()
    if chef:
        profile_data = {
            "username": chef.username,
            "bio": chef.bio,
            "profile_picture": chef.profile_picture,
            "whatsapp": chef.whatsapp,
            "location_enabled": chef.location_enabled
        }
        return jsonify(profile_data)
    return jsonify({"error": "Profile not found"}), 404

@chef_bp.route('/api/chef/update-profile', methods=['POST'])
@login_required
def update_profile():
    """
    Update the profile information for the logged-in chef.
    """
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Parse form data from the request
    username = request.form.get('username')
    bio = request.form.get('bio')
    whatsapp = request.form.get('whatsapp')
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
        chef.profile_picture = filename

    # Update chef information
    chef.username = username
    chef.bio = bio
    chef.whatsapp = whatsapp
    chef.location_enabled = location_enabled
    db.session.commit()

    return jsonify({"success": "Profile updated successfully"})

