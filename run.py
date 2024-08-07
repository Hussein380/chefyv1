from app import app
'''
Imports the app instance from app.py.
Runs the application if the script is executed directly.
'''
if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for development; use a WSGI server in production

