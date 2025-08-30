from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from app.models.project import Project
from app.models.message import Message
from app.models.comment import Comment
from app import db  # Add this import
from datetime import datetime
import traceback  # Add this for better error tracking
import os  # Add this import for os.path.join
from flask import send_from_directory, current_app


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    return render_template('home.html', projects=projects)

@main_bp.route('/projects')
def projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=projects)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        service_type = request.form.get('service_type', '').strip()
        message_content = request.form.get('message', '').strip()
        
        if not all([name, email, message_content]):
            flash('Please fill in all required fields.', 'error')
            return render_template('contact.html', current_year=datetime.now().year)
        
        try:
            # Create message instance
            message = Message(
                name=name,
                email=email,
                phone=phone,
                service_type=service_type,
                message=message_content
            )
            
            # Directly use session operations
            db.session.add(message)
            db.session.commit()
            
            print(f"Message saved: {name}, {email}")
            flash('Your message has been sent! We will contact you soon.', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            db.session.rollback()  # Roll back on error
            error_details = traceback.format_exc()
            print(f"ERROR saving message: {str(e)}\n{error_details}")
            flash(f'Error sending message: {str(e)}', 'error')
    
    # Define service types for the dropdown
    service_types = [
        'Interior Painting',
        'Exterior Painting',
        'Commercial Painting',
        'Decorative Finishes',
        'Cabinet Refinishing',
        'Wallpaper Installation',
        'Color Consultation',
        'Other'
    ]
    
    return render_template('contact.html', service_types=service_types, current_year=datetime.now().year)

@main_bp.route('/comment', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        content = request.form.get('content', '').strip()
        client_type = request.form.get('client_type', '').strip()
        project_id = request.form.get('project_id')  # Optional project association
        
        if not all([name, email, content]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('main.home'))
        
        try:
            # Create comment instance
            comment = Comment(
                name=name,
                email=email,
                content=content,
                client_type=client_type,
                project_id=int(project_id) if project_id else None
            )
            
            # Save to database
            if comment.save():
                print(f"Comment saved: {name}, {email}")
                flash('Your comment has been submitted and is awaiting approval.', 'success')
            else:
                flash('Error submitting comment. Please try again.', 'error')
                
        except Exception as e:
            print(f"ERROR saving comment: {str(e)}")
            flash(f'Error submitting comment: {str(e)}', 'error')
        
        return redirect(url_for('main.home'))

@main_bp.route('/about')
def about():
    """About us page"""
    return render_template('about.html')

# Update any email sending code
def send_contact_email(message):
    recipient_email = "Colour&craft@gmail.com"  # Updated email
    # ... rest of email sending code

@main_bp.route('/favicon.ico')
def favicon():
    """Serve favicon from root URL"""
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', 'favicon'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )