def test_signup(client):
    """
    Test the sign-up functionality.
    """
    response = client.post('/auth/signup', json={
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'consumer'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'User created'

def test_login(client):
    """
    Test the login functionality.
    """
    # First, sign up a user
    client.post('/auth/signup', json={
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'consumer'
    })

    # Then, test login
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    print(response.json)
    assert response.status_code == 200
    assert 'redirect_url' in response.json

