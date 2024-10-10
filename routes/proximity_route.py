from flask import Blueprint, session, jsonify
from models.chef import Chef  # Assuming Chef model is in models.py
import math

# Blueprint for proximity-related routes
proximity_bp = Blueprint('proximity_bp', __name__)

# Haversine formula to calculate the great-circle distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on the Earth's surface using the Haversine formula.
    :param lat1: Latitude of the first point
    :param lon1: Longitude of the first point
    :param lat2: Latitude of the second point
    :param lon2: Longitude of the second point
    :return: Distance between the two points in kilometers
    """
    EARTH_RADIUS_KM = 6371  # Radius of the Earth in kilometers
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (math.sin(delta_lat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c  # Distance in kilometers

# Route to retrieve nearby chefs based on the consumer's current location
@proximity_bp.route('/api/nearby-chefs', methods=['GET'])
def find_nearby_chefs():
    """
    Find and return chefs located near the logged-in consumer.
    Gradually expand the search radius if no chefs are found within the initial distance.
    """
    # Retrieve the consumer's current location (latitude and longitude) from the session
    consumer_latitude = session.get('latitude')  # Consumer's latitude stored in session
    consumer_longitude = session.get('longitude')  # Consumer's longitude stored in session

    # Check if consumer's location is available and valid
    if consumer_latitude is None or consumer_longitude is None:
        return jsonify({"error": "Consumer location not set"}), 400

    try:
        consumer_latitude = float(consumer_latitude)
        consumer_longitude = float(consumer_longitude)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid latitude or longitude'}), 400

    # Retrieve all chefs from the database
    all_chefs = Chef.query.all()

    # Initial search radius (in kilometers)
    search_radius = 10
    max_radius = 100  # Define a maximum limit for expanding the search radius
    radius_increment = 10  # Define how much to increase the radius each time

    # Iterate to expand the search radius if no chefs are found
    while search_radius <= max_radius:
        nearby_chefs = []

        # Iterate through the list of chefs and calculate their distance to the consumer
        for chef in all_chefs:
            # Ensure the chef has a valid location
            if chef.latitude is None or chef.longitude is None:
                continue  # Skip the chef with missing location

            # Calculate distance between the consumer and the chef
            distance_to_chef = calculate_distance(
                consumer_latitude, consumer_longitude,
                chef.latitude, chef.longitude
            )

            # If the chef is within the current search radius, add them to the list
            if distance_to_chef <= search_radius:
                nearby_chefs.append({
                    'chef_id': chef.chef_id,
                    'username': chef.username,
                    'bio': chef.bio or 'No bio available',
                    'profile_image': chef.profile_picture or 'static/assets/default_profile.png',
                    'specialties': chef.cuisine_types.split(',') if chef.cuisine_types else [],  # Split specialties
                    'whatsapp': chef.whatsapp or 'Not provided',
                    'distance_km': round(distance_to_chef, 2)  # Rounded distance for better presentation
                })

        # If chefs are found within the current search radius, return them
        if nearby_chefs:
            return jsonify(nearby_chefs)

        # If no chefs are found, increase the search radius and try again
        search_radius += radius_increment

    # If no chefs were found within the maximum radius, return a message
    return jsonify({"message": "No chefs found within the maximum distance."}), 200

