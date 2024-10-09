import pytest
from flask import session
from models.chef import Chef  # Assuming Chef model is defined in models.chef
from routes.proximity_route import proximity_bp
from app import db  # Import the db instance from your application

# Register the proximity blueprint with the app
@pytest.fixture
def app(client):
    """Register the proximity blueprint with the test client."""
    client.application.register_blueprint(proximity_bp)
    return client.application

def test_missing_consumer_location(client):
    """Test response when the consumer's location is missing."""
    response = client.get('/api/nearby-chefs')
    assert response.status_code == 400
    assert response.json == {'error': 'Consumer location not set'}

def test_invalid_latitude_longitude(client):
    """Test response with invalid latitude and longitude."""
    with client.session_transaction() as sess:
        sess['latitude'] = 'invalid'
        sess['longitude'] = 'invalid'

    response = client.get('/api/nearby-chefs')
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid latitude or longitude'}

def test_no_chefs_in_database(client):
    """Test response when there are no chefs in the database."""
    with client.session_transaction() as sess:
        sess['latitude'] = 34.0522  # Example latitude
        sess['longitude'] = -118.2437  # Example longitude

    response = client.get('/api/nearby-chefs')
    assert response.status_code == 200
    assert response.json == []

"""
def test_chefs_outside_max_distance(client, app):
    Test response when chefs are outside the maximum distance.
    with client.session_transaction() as sess:
        sess['latitude'] = 34.0522  # Example consumer location (Los Angeles)
        sess['longitude'] = -118.2437  # Example consumer location (Los Angeles)
    
    with app.app_context():  # Use the app fixture here
        # Add a chef outside the maximum distance (e.g., New York)
        new_chef = Chef(username='ChefNY', bio='New York Chef', latitude=40.7128, longitude=-74.0060)
        db.session.add(new_chef)  # Ensure save method persists the chef in the database
        db.session.commit()

    response = client.get('/api/nearby-chefs')
    assert response.status_code == 200
    assert len(response.json) == 0  # No chefs within the max distance
"""

"""
def test_chefs_within_max_distance(client, app):
    Test response when there are chefs within the maximum distance.
    with client.session_transaction() as sess:
        sess['latitude'] = 34.0522  # Example consumer location (Los Angeles)
        sess['longitude'] = -118.2437  # Example consumer location (Los Angeles)

    with app.app_context():  # Use the app fixture here
        # Add a chef within the maximum distance (e.g., in Los Angeles)
        new_chef = Chef(username='ChefLA', bio='Los Angeles Chef', latitude=34.0525, longitude=-118.2435)
        db.session.add(new_chef)  # Use db.session.add to persist the chef
        db.session.commit()

    response = client.get('/api/nearby-chefs')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['username'] == 'ChefLA'  # Verify the correct chef is returned
"""
"""
def test_multiple_chefs_at_same_distance(client, app):
    Test response with multiple chefs at the same distance.
    with client.session_transaction() as sess:
        sess['latitude'] = 34.0522  # Example consumer location (Los Angeles)
        sess['longitude'] = -118.2437  # Example consumer location (Los Angeles)

    with app.app_context():  # Use the app fixture here
        # Add two chefs at the same distance from the consumer
        chef1 = Chef(username='Chef1', bio='Chef One', latitude=34.0523, longitude=-118.2438)
        chef2 = Chef(username='Chef2', bio='Chef Two', latitude=34.0523, longitude=-118.2439)
        db.session.add(chef1)  # Use db.session.add to persist the chefs
        db.session.add(chef2)
        db.session.commit()

    response = client.get('/api/nearby-chefs')
    assert response.status_code == 200
    assert len(response.json) == 2  # Both chefs should be returned
    usernames = [chef['username'] for chef in response.json]
    assert 'Chef1' in usernames
    assert 'Chef2' in usernames
"""
