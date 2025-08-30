import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models import Project  # Import the Project model
from app import db  # Import the db object

admin_bp = Blueprint('admin', __name__)

UPLOAD_FOLDER = 'app/static/uploads/projects'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/admin/project/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image_url = request.form.get('image_url')
        category = request.form.get('category')

        # Handle file upload
        file = request.files.get('image_file')
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{int(datetime.utcnow().timestamp())}_{filename}"
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            image_url = f'/static/uploads/projects/{filename}'

        project = Project(
            title=title,
            description=description,
            image_url=image_url,
            category=category
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/project_edit.html')