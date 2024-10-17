from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template  # Added render_template
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app import db
from models.dishes import Dishes
from models.chef import Chef
import os

dish_bp = Blueprint('dish_bp', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dish_bp.route('/api/dish/add', methods=['POST'])
@login_required
def add_dish():
    if 'dish_image' not in request.files:
        flash('No file part')
        return redirect(url_for('dish_bp.list_dishes'))  # Redirect to list_dishes if no file

    dish_image = request.files['dish_image']
    if dish_image.filename == '':
        flash('No selected file')
        return redirect(url_for('dish_bp.list_dishes'))

    if dish_image and allowed_file(dish_image.filename):
        filename = secure_filename(dish_image.filename)
        dish_image.save(os.path.join(UPLOAD_FOLDER, filename))

        dish_name = request.form.get('dish_name')
        dish_price = request.form.get('dish_price', type=float)
        dish_quantity = request.form.get('quantity', type=int)

        if dish_quantity is None or dish_quantity <= 0:
            flash('Quantity must be greater than zero.')
            return redirect(url_for('dish_bp.list_dishes'))

        chef = Chef.query.filter_by(user_id=current_user.id).first()
        if chef:
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
            flash('Dish added successfully!')
            return redirect(url_for('dish_bp.list_dishes'))

        flash("Chef profile not found")
    else:
        flash('File type not allowed')

    return redirect(url_for('dish_bp.list_dishes'))

@dish_bp.route('/api/dishes', methods=['GET'])
def view_dishes():
    dishes = Dishes.query.all()
    return render_template('view_dishes.html', dishes=dishes)

@dish_bp.route('/api/list_dishes', methods=['GET'])
@login_required
def list_dishes():
    chef = Chef.query.filter_by(user_id=current_user.id).first()
    if chef:
        dishes = Dishes.query.filter_by(chef_id=chef.chef_id).all()
        return render_template('list_dishes.html', dishes=dishes)
    else:
        flash("Chef profile not found")
        return redirect(url_for('dish_bp.add_dish'))

@dish_bp.route('/api/dish/<int:dish_id>/delete', methods=['POST'])
@login_required
def delete_dish(dish_id):
    dish = Dishes.query.get_or_404(dish_id)
    db.session.delete(dish)
    db.session.commit()
    flash('Dish deleted successfully!')
    return redirect(url_for('dish_bp.list_dishes'))

