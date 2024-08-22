import pytest
from app import create_app, db

@pytest.fixture
def client():
    """
    Fixture for creating a test client with a fresh database for each test.
    """
    # Create a Flask app instance for testing
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Set up the test client and create a database schema
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for testing
        # Run the tests
        yield client
        with app.app_context():
            db.drop_all()  # Drop tables after testing

