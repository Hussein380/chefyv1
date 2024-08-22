from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from models import db
from models.chef import Chef
from models.dishes import Dishes
from models.order import Order
from models.review import Review
from models.user import User

# Define a blueprint for the chef routes
chef_bp = Blueprint('chef', __name__)

# Route for the Chef Dashboard
@chef_bp.route('/dashboard/chef', methods=['GET'])
@login_required  # Ensure only logged-in users can access this route
def chef_dashboard():
    """
    Displays the chef's dashboard with an overview of their dishes, orders, and reviews.

    - Fetches the logged-in chef's data using the current user's ID.
    - Retrieves related dishes, orders, and reviews from the database.
    - Renders the 'chef_dashboard.html' template with the fetched data.
    """
    chef = Chef.query.get(current_user.id)
    # If the chef does not exist, return an empty list to avoid errors
    dishes = chef.dishes if chef else []
    orders = Order.query.filter_by(chef_id=current_user.id).all()
    reviews = Review.query.filter_by(chef_id=current_user.id).all()

    return render_template('chef_dashboard.html', chef=chef, dishes=dishes, orders=orders, reviews=reviews)

# Route to update chef profile
@chef_bp.route('/dashboard/chef/profile', methods=['POST'])
@login_required
def update_chef_profile():
    """
    Updates the chef's profile information.

    - Fetches the logged-in chef's data from the database.
    - Updates the profile fields (username, email, bio) based on form input.
    - Handles profile picture upload if provided.
    - Commits the changes to the database.
    - Redirects back to the dashboard with a success message.
    """
    chef = Chef.query.get(current_user.id)
    if not chef:
        flash('Chef not found', 'error')
        return redirect(url_for('chef.chef_dashboard'))

    # Update chef profile information
    chef.user.username = request.form.get('username', chef.user.username)
    chef.bio = request.form.get('bio', chef.bio)
    chef.user.email = request.form.get('email', chef.user.email)

    # Handle profile picture upload
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and file.filename:
            filename = secure_filename(file.filename)
            # Save the uploaded file to the 'static/uploads' folder
            file.save(os.path.join('static/uploads', filename))
            chef.profile_picture = filename

    # Save changes to the database
    db.session.commit()
    flash('Profile updated successfully', 'success')

    return redirect(url_for('chef.chef_dashboard'))

@chef_bp.route('/dashboard/chef/dishes', methods=['POST'])
@login_required
def add_dish():
    # Your implementation for adding a dish
    pass

# Route for managing dishes (display and add)
@chef_bp.route('/dashboard/chef/dishes', methods=['GET', 'POST'])
@login_required
def manage_dishes():
    """
    Manages the chef's dishes: displays current dishes and handles adding new ones.

    - On GET request: Displays the list of dishes.
    - On POST request: Handles adding a new dish based on form input.
    - Handles dish image upload if provided.
    - Commits the new dish to the database and redirects with a success message.
    """
    chef = Chef.query.get(current_user.id)
    if not chef:
        flash('Chef not found', 'error')
        return redirect(url_for('chef.chef_dashboard'))

    if request.method == 'POST':
        # Get form data for the new dish
        dish_name = request.form.get('dishName')
        description = request.form.get('dishDescription')
        price = request.form.get('price')
        quantity = request.form.get('quantity')

        # Handle dish image upload
        dish_image = None
        if 'dishImage' in request.files:
            file = request.files['dishImage']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Save the uploaded image to 'static/uploads'
                file.save(os.path.join('static/uploads', filename))
                dish_image = filename

        # Create a new Dish instance and save it to the database
        new_dish = Dishes(
            name=dish_name,
            description=description,
            price=price,
            quantity=quantity,
            image=dish_image,
            chef_id=current_user.id
        )
        db.session.add(new_dish)
        db.session.commit()
        flash('Dish added successfully', 'success')
        return redirect(url_for('chef.chef_dashboard'))

    return render_template('chef_dashboard.html', dishes=chef.dishes)

# Route to update an existing dish
@chef_bp.route('/dashboard/chef/dishes/edit/<int:dish_id>', methods=['POST'])
@login_required
def edit_dish(dish_id):
    """
    Updates an existing dish's information.

    - Fetches the dish by its ID and verifies it belongs to the logged-in chef.
    - Updates dish fields (name, description, price, quantity) based on form input.
    - Handles dish image update if provided.
    - Commits the changes to the database and redirects with a success message.
    """
    dish = Dishes.query.get(dish_id)
    # Check if the dish exists and belongs to the current chef
    if not dish or dish.chef_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('chef.chef_dashboard'))

    # Update dish information based on form input
    dish.name = request.form.get('dishName', dish.name)
    dish.description = request.form.get('dishDescription', dish.description)
    dish.price = request.form.get('price', dish.price)
    dish.quantity = request.form.get('quantity', dish.quantity)

    # Handle dish image update
    if 'dishImage' in request.files:
        file = request.files['dishImage']
        if file and file.filename:
            filename = secure_filename(file.filename)
            # Save the updated image to 'static/uploads'
            file.save(os.path.join('static/uploads', filename))
            dish.image = filename

    # Save the updated dish to the database
    db.session.commit()
    flash('Dish updated successfully', 'success')
    return redirect(url_for('chef.chef_dashboard'))

# Route to delete a dish
@chef_bp.route('/dashboard/chef/dishes/delete/<int:dish_id>', methods=['POST'])
@login_required
def delete_dish(dish_id):
    """
    Deletes a dish from the chef's list.

    - Fetches the dish by its ID and verifies it belongs to the logged-in chef.
    - Deletes the dish from the database and commits the change.
    - Redirects back to the dashboard with a success message.
    """
    dish = Dishes.query.get(dish_id)
    # Check if the dish exists and belongs to the current chef
    if not dish or dish.chef_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('chef.chef_dashboard'))

    # Delete the dish and save the change to the database
    db.session.delete(dish)
    db.session.commit()
    flash('Dish deleted successfully', 'success')
    return redirect(url_for('chef.chef_dashboard'))

# Route for managing orders
@chef_bp.route('/dashboard/chef/orders', methods=['GET'])
@login_required
def manage_orders():
    """
    Displays the chef's orders.

    - Fetches all orders assigned to the logged-in chef.
    - Renders the 'chef_dashboard.html' template with the orders data.
    """
    chef = Chef.query.get(current_user.id)
    if not chef:
        flash('Chef not found', 'error')
        return redirect(url_for('chef.chef_dashboard'))

    orders = Order.query.filter_by(chef_id=current_user.id).all()
    return render_template('chef_dashboard.html', orders=orders)

# Route to update the status of an order
@chef_bp.route('/dashboard/chef/orders/update/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    """
    Updates the status of an order.

    - Fetches the order by its ID and verifies it belongs to the logged-in chef.
    - Updates the order status based on form input.
    - Commits the changes to the database and redirects with a success message.
    """
    order = Order.query.get(order_id)
    # Check if the order exists and belongs to the current chef
    if not order or order.chef_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('chef.chef_dashboard'))

    # Update the order status
    order.status = request.form.get('status', order.status)
    db.session.commit()
    flash('Order status updated successfully', 'success')
    return redirect(url_for('chef.chef_dashboard'))

# Route for managing reviews
@chef_bp.route('/dashboard/chef/reviews', methods=['GET'])
@login_required
def manage_reviews():
    """
    Displays the chef's reviews.

    - Fetches all reviews related to the logged-in chef.
    - Renders the 'chef_dashboard.html' template with the reviews data.
    """
    chef = Chef.query.get(current_user.id)
    if not chef:
        flash('Chef not found', 'error')
        return redirect(url_for('chef.chef_dashboard'))

    reviews = Review.query.filter_by(chef_id=current_user.id).all()
    return render_template('chef_dashboard.html', reviews=reviews)

# Route to create a new chef
@chef_bp.route('/chef', methods=['POST'])
@login_required
def create_chef():
    """
    Creates a new chef.
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    bio = data.get('bio')
    profile_picture = data.get('profile_picture')

    if role != 'chef':
        return jsonify({'message': 'Invalid role'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username, email=email, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    new_chef = Chef(user_id=new_user.id, bio=bio, profile_picture=profile_picture)
    db.session.add(new_chef)
    db.session.commit()

    return jsonify({'message': 'Chef created successfully'}), 201

# Route to get a chef's details
@chef_bp.route('/chef/<int:chef_id>', methods=['GET'])
@login_required
def get_chef(chef_id):
    """
    Retrieves a chef's details.
    """
    chef = Chef.query.get(chef_id)
    if not chef:
        return jsonify({'message': 'Chef not found'}), 404

    return jsonify({
        'username': chef.user.username,
        'email': chef.user.email,
        'bio': chef.bio,
        'profile_picture': chef.profile_picture,
        'rating': chef.rating
    }), 200

# Route to update a chef's details
@chef_bp.route('/chef/<int:chef_id>', methods=['PUT'])
@login_required
def update_chef(chef_id):
    """
    Updates a chef's details.
    """
    chef = Chef.query.get(chef_id)
    if not chef:
        return jsonify({'message': 'Chef not found'}), 404

    data = request.get_json()
    chef.bio = data.get('bio', chef.bio)
    chef.profile_picture = data.get('profile_picture', chef.profile_picture)
    chef.rating = data.get('rating', chef.rating)

    db.session.commit()

    return jsonify({'message': 'Chef updated successfully'}), 200

# Route to delete a chef
@chef_bp.route('/chef/<int:chef_id>', methods=['DELETE'])
@login_required
def delete_chef(chef_id):
    """
    Deletes a chef.
    """
    chef = Chef.query.get(chef_id)
    if not chef:
        return jsonify({'message': 'Chef not found'}), 404

    db.session.delete(chef)
    db.session.commit()

    return jsonify({'message': 'Chef deleted successfully'}), 200

