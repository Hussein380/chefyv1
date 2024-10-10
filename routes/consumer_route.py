from flask import Blueprint, jsonify
from models.chef import Chef  # Ensure the Chef model is correctly imported

# Define the Blueprint
consumer_bp = Blueprint('consumer', __name__)

@consumer_bp.route('/api/chefs', methods=['GET'])
def get_chefs():
    try:
        # Retrieve all chefs from the database
        chefs = Chef.query.all()

        # Format the chef data to return
        chefs_data = [
            {
                'id': chef.chef_id,
                'name': chef.username,
                'image': chef.profile_picture or 'static/assets/default_profile.png',  # Default image
                'bio': chef.bio,
                'specialties': chef.cuisine_types.split(',') if chef.cuisine_types else [],  # Split specialties
                'whatsapp': chef.whatsapp
            }
            for chef in chefs
        ]

        return jsonify(chefs_data), 200  # Return the data as JSON
    except Exception as e:
        print(f"Error fetching chefs: {e}")
        return jsonify({"error": "Unable to fetch chefs."}), 500  # Return an error message

