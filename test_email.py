from flask import Flask
from flask_mail import Mail, Message
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

def send_test_email():
    with app.app_context():  # Ensure this block is within the application context
        msg = Message('Test Email', recipients=['huznigarane@gmail.com'])
        msg.body = 'This is a test email.'
        try:
            mail.send(msg)
            print('Email sent successfully.')
        except Exception as e:
            print(f'Failed to send email: {e}')

if __name__ == '__main__':
    send_test_email()

