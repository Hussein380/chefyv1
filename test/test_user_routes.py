import sys
import os
import pytest
from app import app, db

# Add the root directory to the Python path to ensure imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    """
    Fixture for creating a test client with a fresh database for each test.
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/HomeMade'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for testing
        yield client
        with app.app_context():
            db.drop_all()  # Drop tables after tests

def test_register_user(client):
    """
    Test the user registration endpoint.
    """
    response = client.post('/user/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'role': 'consumer'
    })
    assert response.status_code == 201  # Check if status code is 201 (Created)
    assert b'User registered successfully' in response.data  # Check for success message

def test_get_user_profile(client):
    """
    Test fetching a user profile.
    """
    # First, register a user to fetch their profile
    client.post('/user/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'role': 'consumer'
    })
    response = client.get('/user/profile/1')  # Fetch user profile
    assert response.status_code == 200  # Check if status code is 200 (OK)
    assert b'testuser' in response.data  # Check if the username is in the response

def test_update_user_profile(client):
    """
    Test updating a user profile.
    """
    # First, register a user to update their profile
    client.post('/user/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'role': 'consumer'
    })
    response = client.put('/user/profile/1', json={
        'username': 'updateduser'
    })  # Update username
    assert response.status_code == 200  # Check if status code is 200 (OK)
    assert b'Profile updated successfully' in response.data  # Check for success message

def test_delete_user_account(client):
    """
    Test deleting a user account.
    """
    # First, register a user to delete their account
    client.post('/user/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'role': 'consumer'
    })
    response = client.delete('/user/profile/1')  # Delete user account
    assert response.status_code == 200  # Check if status code is 200 (OK)
    assert b'Account deleted successfully' in response.data  # Check for success message

