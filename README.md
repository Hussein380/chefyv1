# HomeMade

HomeMade is a web application that connects local chefs with consumers who want to enjoy homemade dishes. The app allows chefs to create profiles, upload dishes, and manage their menus, while consumers can browse chefs, view available dishes, and find chefs closest to them.

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Screenshots](#screenshots)
6. [Contributing](#contributing)
7. [License](#license)

## Features

- **Chef Profiles**: Chefs can create and update their profiles, including uploading profile images.
- **Dish Management**: Chefs can add, update, or delete dishes they offer.
- **Consumer Browsing**: Consumers can browse chef profiles and view available dishes.
- **Geolocation**: Consumers can find the closest chefs to their location using the HTML5 Geolocation API.
- **Authentication**: Secure login and registration for chefs.

## Project Structure

```bash
HomeMade/
│
├── static/                # Static files (CSS, JS, images)
│   ├── assets/            # Profile images, default images, and other static assets
│   ├── scripts/           # JavaScript files
│   │   └── chef_dashboard.js  # JavaScript file for the chef dashboard
│   └── styles/            # CSS files
│       └── style.css      # Main stylesheet for the app
│
├── templates/             # HTML templates
│   ├── base.html          # Base layout template
│   ├── consumer_page.html # Consumer-facing page displaying chef profiles
│   ├── chef_dashboard.html # Chef dashboard page for profile and dish management
│   ├── view_dishes.html   # Page displaying a list of dishes offered by chefs
│   └── auth/              # Authentication templates (login, register, etc.)
│       ├── login.html     # Login page for chefs
│       └── register.html  # Registration page for chefs
│
├── models/                # Database models
│   ├── chef.py            # Chef model (includes fields for latitude, longitude, profile info)
│   ├── dishes.py          # Dish model (stores chef dishes)
│   └── __init__.py        # Initialize models
│
├── routes/                # Route handlers (Flask views)
│   ├── chef_route.py      # Routes related to chef actions (profile management, etc.)
│   ├── dish_route.py      # Routes related to dish management
│   ├── consumer_route.py  # Routes for consumer-facing pages and actions
│   └── auth.py            # Authentication routes (login, registration)
│
├── migrations/            # Database migrations (handled by Flask-Migrate)
├── config.py              # Configuration file (database connection, secret keys, etc.)
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

```
## Installation

To set up the HomeMade application on your local machine, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/HomeMade.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd HomeMade
    ```

3. **Create a virtual environment**:

    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment**:

    - On **macOS/Linux**:

      ```bash
      source venv/bin/activate
      ```

    - On **Windows**:

      ```bash
      venv\Scripts\activate
      ```

5. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

6. **Set up the database** by running the following commands:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

7. **Run the Flask app**:

    ```bash
    flask run
    ```

    The app will now be running at `http://127.0.0.1:5000/`.

---

## Usage

Once the app is running, here’s how to use the main features:

### For Chefs:
- **Create and manage your profile**: Chefs can update their personal details and upload a profile image.
- **Dish management**: Add, edit, or delete dishes on your menu.
- **Set your location**: Use latitude and longitude to define your location for consumers.

### For Consumers:
- **Browse chefs**: See a list of chefs and explore their profiles.
- **View dishes**: Check out dishes available from each chef.
- **Geolocation feature**: Find chefs nearest to your location using HTML5 Geolocation API.

---

## Screenshots

*Screenshots will be added here soon.*

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork the repository**.
2. **Create a new branch** for your feature or bug fix:
   
    ```bash
    git checkout -b your-branch-name
    ```

3. **Commit your changes** with a clear message:

    ```bash
    git commit -m "Description of your feature or fix"
    ```

4. **Push to the branch**:

    ```bash
    git push origin your-branch-name
    ```

5. **Submit a pull request**: Once your changes are complete and tested, open a pull request for review.

---

## License

This project is licensed under the MIT License.




Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add feature').
Push to the branch (git push origin feature-branch).
Create a pull request.
License
This project is licensed under the MIT License.
