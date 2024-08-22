from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db
from models.media import Media
from models.chef import Chef

media_bp = Blueprint('media', __name__)

@media_bp.route('/dashboard/chef/media', methods=['GET'])
@login_required
def get_media():
    chef = Chef.query.get(current_user.id)
    if not chef:
        flash('Chef not found', 'error')
        return redirect(url_for('chef.chef_dashboard'))

    media = Media.query.filter_by(chef_id=current_user.id).all()
    return render_template('chef_media.html', media=media)

@media_bp.route('/dashboard/chef/media/upload', methods=['POST'])
@login_required
def upload_media():
    chef = Chef.query.get(current_user.id)
    if not chef:
        flash('Chef not found', 'error')
        return redirect(url_for('chef.chef_dashboard'))

    if 'media_file' in request.files:
        file = request.files['media_file']
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/uploads', filename))

            media_type = request.form.get('media_type')
            new_media = Media(
                media_url=filename,
                media_type=media_type,
                chef_id=current_user.id
            )
            db.session.add(new_media)
            db.session.commit()
            flash('Media uploaded successfully', 'success')
            return redirect(url_for('media.get_media'))

    flash('No file selected', 'error')
    return redirect(url_for('media.get_media'))

@media_bp.route('/dashboard/chef/media/update/<int:media_id>', methods=['POST'])
@login_required
def update_media(media_id):
    media = Media.query.get(media_id)
    if not media or media.chef_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('media.get_media'))

    media.media_url = request.form.get('media_url', media.media_url)
    media.media_type = request.form.get('media_type', media.media_type)
    db.session.commit()
    flash('Media updated successfully', 'success')
    return redirect(url_for('media.get_media'))

@media_bp.route('/dashboard/chef/media/delete/<int:media_id>', methods=['POST'])
@login_required
def delete_media(media_id):
    media = Media.query.get(media_id)
    if not media or media.chef_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('media.get_media'))

    db.session.delete(media)
    db.session.commit()
    flash('Media deleted successfully', 'success')
    return redirect(url_for('media.get_media'))

