from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app import db
from models.dishes import Dishes  # Ensure you import the Dishes model correctly
from models.chef import Chef
import os

dish_bp = Blueprint('dish_bp', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dish_bp.route('/api/dish/add', methods=['POST'])
@login_required
def add_dish():
    if 'dish_image' not in request.files:
        flash('No file part')
        return redirect(request.url)

    dish_image = request.files['dish_image']

    if dish_image.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if dish_image and allowed_file(dish_image.filename):
        filename = secure_filename(dish_image.filename)
        dish_image.save(os.path.join(UPLOAD_FOLDER, filename))

        dish_name = request.form.get('dish_name')
        dish_price = request.form.get('dish_price', type=float)
        dish_quantity = request.form.get('quantity', type=int)  # Retrieve quantity as integer

        if dish_quantity is None:  # Check if quantity was provided
            flash('Quantity is required.')
            return redirect(request.url)

        chef = Chef.query.filter_by(user_id=current_user.id).first()
        if chef:
            # Instantiate the Dishes model
            new_dish = Dishes(
                    dish_name=dish_name,
                    dish_image=filename,
                    price=dish_price,
                    quantity=dish_quantity,
                    chef_id=chef.chef_id,
                    likes=0  # Initialize likes to 0
        )
            db.session.add(new_dish)
            db.session.commit()
        else:
            flash("chef profile not found")


        flash('Dish added successfully!')
        return redirect(url_for('dish_bp.view_dishes'))

    flash('File type not allowed')
    return redirect(request.url)

@dish_bp.route('/api/dishes', methods=['GET'])
def view_dishes():
    print("View dishes route accessed")
    chef_id =  request.args.get('chef_id')
    if chef_id:
        # fetch dishes specific to that chef
        dishes = Dishes.query.filter_by(chef_id=chef_id).all()
    else:
        dishes = Dishes.query.all()
    return render_template('view_dishes.html', dishes=dishes)

@dish_bp.route('/api/dish/<int:dish_id>/like', methods=['POST'])
@login_required
def like_dish(dish_id):
    # Find the dish by ID
    dish = Dishes.query.get_or_404(dish_id)
    
    # Increment the likes count
    dish.likes += 1
    db.session.commit()
    
    return jsonify({'likes': dish.likes})  # Return updated likes count

