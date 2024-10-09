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
    The consumer's location is retrieved from the session, and the distance is calculated using the Haversine formula.
    Chefs within a specified distance (e.g., 10 km) are returned.

    :return: A JSON response containing nearby chefs' profiles and the calculated distance to the consumer
    """
    # Retrieve the consumer's current location (latitude and longitude) from the session
    consumer_latitude = session.get('latitude')  # Consumer's latitude stored in session
    consumer_longitude = session.get('longitude')  # Consumer's longitude stored in session

    # check if consumer's location is available and valid
    if consumer_latitude is None or consumer_longitude is None:
        return jsonify({"error": "Consumer location not set"}), 400

    try:
        consumer_latitude = float(consumer_latitude)
        consumer_longitude = float(consumer_longitude)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid latitude or longitude'}), 400


    # Check if consumer's location is available
    if not consumer_latitude or not consumer_longitude:
        return jsonify({'error': 'Consumer location not available'}), 400

    # Retrieve all chefs from the database
    all_chefs = Chef.query.all()
    nearby_chefs = []

    # Define the maximum distance (in kilometers) to consider as "nearby"
    MAX_DISTANCE_KM = 10

    # Iterate through the list of chefs and calculate their distance to the consumer
    for chef in all_chefs:
        # Calculate distance between the consumer and the chef
        distance_to_chef = calculate_distance(
            float(consumer_latitude), float(consumer_longitude), 
            chef.latitude, chef.longitude
        )

        # If the chef is within the maximum distance, add them to the list of nearby chefs
        if distance_to_chef <= MAX_DISTANCE_KM:
            nearby_chefs.append({
                'chef_id': chef.id,
                'username': chef.username,
                'bio': chef.bio,
                'profile_picture': chef.profile_picture,
                'distance_km': round(distance_to_chef, 2)  # Rounded distance for better presentation
            })

    # Return the list of nearby chefs as a JSON response
    return jsonify(nearby_chefs)

