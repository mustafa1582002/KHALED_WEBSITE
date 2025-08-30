from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, current_app
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from functools import wraps  # Add this import
import os
import hashlib
import secrets
import re
import logging
import base64
from uuid import uuid4

from app.models.project import Project
from app.models.message import Message
from app.models.comment import Comment
from app.models.admin_user import AdminUser
from app import db

# Define login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in first.', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

admin_bp = Blueprint('admin', __name__)

# Secret admin access key
ADMIN_ACCESS_KEY = "color-craft-admin-2024"

# Security logging
security_logger = logging.getLogger('admin_security')
handler = logging.FileHandler('admin_security.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
security_logger.addHandler(handler)
security_logger.setLevel(logging.INFO)

def log_security_event(event_type, details, ip_address=None):
    """Log security events"""
    ip = ip_address or request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    message = f"{event_type} - IP: {ip} - {details}"
    security_logger.info(message)
    print(f"🔒 SECURITY: {message}")

def generate_secure_token():
    return secrets.token_urlsafe(32)

# SECURITY CHECK FOR ALL ADMIN ROUTES
@admin_bp.before_request
def check_admin_security():
    """STRICT security check for ALL admin routes"""
    
    # Routes that don't require login
    ALLOWED_WITHOUT_LOGIN = [
        'admin.secure_admin_access',
        'admin.login',  # Add login to allowed routes
    ]
    
    # Check if this is an admin route
    if request.endpoint and 'admin' in request.endpoint:
        print(f"🔒 Security check for: {request.endpoint}")
        
        # Allow these routes without login
        if request.endpoint in ALLOWED_WITHOUT_LOGIN:
            print(f"✅ Route {request.endpoint} allowed without login")
            return
        
        # ALL OTHER ADMIN ROUTES REQUIRE LOGIN
        if not session.get('admin_logged_in'):
            print(f"❌ BLOCKED: {request.endpoint} - not logged in")
            log_security_event("UNAUTHORIZED_ACCESS", f"Access attempt to {request.endpoint}", request.remote_addr)
            flash('Access denied.', 'error')
            return redirect(url_for('main.home'))
        
        # Check session timeout for logged-in users
        login_time = session.get('admin_login_time')
        if login_time:
            try:
                login_datetime = datetime.fromisoformat(login_time)
                if datetime.now() - login_datetime > timedelta(hours=4):
                    print("❌ Session expired")
                    session.clear()
                    log_security_event("SESSION_EXPIRED", "Session timeout", request.remote_addr)
                    flash('Session expired.', 'warning')
                    return redirect(url_for('main.home'))
            except ValueError:
                print("❌ Invalid session timestamp")
                session.clear()
                return redirect(url_for('main.home'))
        
        print(f"✅ Security check passed for {request.endpoint}")

# SECURE ADMIN ACCESS ROUTE
@admin_bp.route('/secure-admin-access/<access_key>')
def secure_admin_access(access_key):
    """Secure admin access with secret key"""
    print(f"🔑 Secure access attempt with key: {access_key}")
    
    if access_key != ADMIN_ACCESS_KEY:
        print(f"❌ Invalid access key: {access_key}")
        abort(404)
    
    print("✅ Valid access key, setting session flag and redirecting to login")
    # Set a session flag to indicate valid access
    session['valid_admin_access'] = True
    flash('Access granted! Please login.', 'success')
    return redirect(url_for('admin.login'))

# ADMIN LOGIN
@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Admin login with database authentication"""
    print("Admin login route accessed")
    
    # Check if user has valid access or is already logged in
    if not session.get('admin_logged_in') and not session.get('valid_admin_access'):
        print("❌ Direct login access blocked - no valid access token")
        log_security_event("UNAUTHORIZED_LOGIN_ACCESS", "Direct admin login attempt", request.remote_addr)
        flash('Page not found.', 'error')
        return redirect(url_for('main.home'))
    
    # If already logged in, redirect to dashboard
    if session.get('admin_logged_in'):
        login_time = session.get('admin_login_time')
        if login_time:
            try:
                login_datetime = datetime.fromisoformat(login_time)
                if datetime.now() - login_datetime > timedelta(hours=4):
                    print("Session expired, clearing session")
                    session.clear()
                else:
                    print("Valid session found, redirecting to dashboard")
                    return redirect(url_for('admin.dashboard'))
            except ValueError:
                print("Invalid session timestamp, clearing session")
                session.clear()
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        print(f"Login attempt - Username: '{username}', Password length: {len(password)}")
        
        # Try database authentication first
        try:
            admin_user, message = AdminUser.authenticate(username, password)
            if admin_user:
                print("✅ Database authentication successful")
                
                # Create session
                session.permanent = True
                session['admin_logged_in'] = True
                session['admin_username'] = username
                session['admin_user_id'] = admin_user.id  # Store user ID
                session['admin_login_time'] = datetime.now().isoformat()
                session['admin_token'] = generate_secure_token()
                session['csrf_token'] = session['admin_token']
                
                # Clear the access flag
                session.pop('valid_admin_access', None)
                
                print("✅ Session created successfully")
                flash('Welcome to the admin panel!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                print(f"❌ Database authentication failed: {message}")
                flash('Invalid username or password. Please try again.', 'error')
                
        except Exception as e:
            print(f"❌ Database error during authentication: {str(e)}")
            
            # Fallback to hardcoded admin for emergency access
            if username == 'admin' and password == 'admin123':
                print("✅ Fallback authentication successful")
                
                session.permanent = True
                session['admin_logged_in'] = True
                session['admin_username'] = username
                session['admin_user_id'] = 1  # Default admin user ID
                session['admin_login_time'] = datetime.now().isoformat()
                session['admin_token'] = generate_secure_token()
                session['csrf_token'] = session['admin_token']
                
                # Clear the access flag
                session.pop('valid_admin_access', None)
                
                flash('Welcome to the admin panel!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Invalid username or password. Please try again.', 'error')
    
    return render_template('admin/login.html')

# ADMIN LOGOUT
@admin_bp.route('/admin/logout')
def logout():
    """Admin logout"""
    username = session.get('admin_username', 'Unknown')
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.home'))

# ADMIN DASHBOARD
@admin_bp.route('/admin/dashboard')
def dashboard():
    """Admin dashboard with accurate statistics"""
    print("Dashboard route accessed")
    
    try:
        # Get projects with better error handling
        projects = []
        projects_count = 0
        
        try:
            # First try the standard query method
            projects = Project.query.order_by(Project.created_at.desc()).all()
            projects_count = len(projects)
            print(f"✅ Found {projects_count} projects using Project.query")
            
        except Exception as e:
            print(f"⚠️ Project.query failed: {e}")
            try:
                # Fallback to get_all method if it exists
                if hasattr(Project, 'get_all'):
                    projects = Project.get_all()
                    projects_count = len(projects)
                    print(f"✅ Found {projects_count} projects using Project.get_all")
                else:
                    print("❌ No Project.get_all method available")
            except Exception as e2:
                print(f"❌ Project.get_all also failed: {e2}")
                projects = []
                projects_count = 0
        
        # Get messages statistics
        messages_count = 0
        unread_count = 0
        try:
            messages_count = Message.query.count()
            unread_count = Message.query.filter_by(is_read=False).count()
        except Exception as e:
            print(f"Error loading messages stats: {e}")
        
        # Get comments statistics
        comments_count = 0
        pending_comments_count = 0
        try:
            comments_count = Comment.query.count()
            pending_comments_count = Comment.query.filter_by(is_approved=False).count()
        except Exception as e:
            print(f"Error loading comments stats: {e}")
        
        # Get admin users count
        admin_users_count = 0
        try:
            admin_users_count = AdminUser.query.count()
        except Exception as e:
            print(f"Error counting admin users: {e}")
        
        # Debug output
        print(f"Dashboard statistics:")
        print(f"  Projects: {projects_count}")
        print(f"  Messages: {messages_count} (Unread: {unread_count})")
        print(f"  Comments: {comments_count} (Pending: {pending_comments_count})")
        print(f"  Admin Users: {admin_users_count}")
        
        if projects_count == 0:
            print("⚠️ No projects found - checking database directly...")
            # Direct database check
            try:
                import mysql.connector
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='GGTAHAEHt.1',
                    database='color_and_craft'
                )
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM projects")
                db_count = cursor.fetchone()[0]
                print(f"   Direct database count: {db_count} projects")
                
                if db_count > 0:
                    cursor.execute("SELECT id, title FROM projects LIMIT 5")
                    sample_projects = cursor.fetchall()
                    print(f"   Sample projects: {sample_projects}")
                
                connection.close()
            except Exception as e:
                print(f"   Database check failed: {e}")
        
        return render_template('admin/dashboard.html', 
                             projects=projects,
                             projects_count=projects_count,
                             messages_count=messages_count,
                             unread_count=unread_count,
                             comments_count=comments_count,
                             pending_comments_count=pending_comments_count,
                             admin_users_count=admin_users_count)
                             
    except Exception as e:
        print(f"Error in dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        
        flash(f'Dashboard error: {str(e)}', 'error')
        return render_template('admin/dashboard.html', 
                             projects=[],
                             projects_count=0,
                             messages_count=0,
                             unread_count=0,
                             comments_count=0,
                             pending_comments_count=0,
                             admin_users_count=0)

# BLOCK COMMON ADMIN URLs
@admin_bp.route('/admin')
@admin_bp.route('/admin/')
@admin_bp.route('/administrator')
@admin_bp.route('/wp-admin')
@admin_bp.route('/admin.php')
def admin_redirect():
    """Block common admin URL attempts"""
    print(f"❌ Blocked admin URL access attempt from: {request.remote_addr}")
    abort(404)

# PROJECT MANAGEMENT ROUTES
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

@admin_bp.route('/admin/project/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    """Edit project with file upload support"""
    project = Project.get_by_id(project_id)
    if not project:
        flash('Project not found!', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        image_url = request.form.get('image_url', '').strip()
        category = request.form.get('category', '').strip()
        
        if not all([title, description]):
            flash('Title and description are required!', 'error')
            return render_template('admin/project_edit.html', project=project)
        
        try:
            # Process image - keep existing if no new image provided
            processed_image_url = process_project_image(image_url, request.files.get('image_file'))
            
            # Use existing image if no new image provided
            if not processed_image_url:
                processed_image_url = project.image_url
            
            project.update(
                title=title, 
                description=description, 
                image_url=processed_image_url,
                category=category if category else project.category
            )
            flash('Project updated successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
            
        except Exception as e:
            print(f"Error updating project: {str(e)}")
            flash(f'Error updating project: {str(e)}', 'error')
    
    return render_template('admin/project_edit.html', project=project)

def process_project_image(image_url, image_file):
    """Process image URL or uploaded file"""
    
    # Priority 1: Uploaded file
    if image_file and image_file.filename:
        try:
            return save_uploaded_image(image_file)
        except Exception as e:
            print(f"Error saving uploaded file: {e}")
            flash(f'Error uploading file: {str(e)}', 'error')
            return None
    
    # Priority 2: Regular URL
    if image_url and not image_url.startswith('data:'):
        if image_url.startswith(('http://', 'https://', '/')):
            print(f"Using provided URL: {image_url[:100]}...")
            return image_url
        else:
            print(f"Invalid URL format: {image_url[:50]}")
            return None
    
    # Priority 3: Base64 data (convert to file)
    if image_url and image_url.startswith('data:image/'):
        try:
            return save_base64_image(image_url)
        except Exception as e:
            print(f"Error processing base64 image: {e}")
            flash(f'Error processing image data: {str(e)}', 'error')
            return None
    
    return None

def save_uploaded_image(image_file):
    """Save uploaded image file"""
    if not image_file or not image_file.filename:
        return None
    
    # Validate file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    filename = secure_filename(image_file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    if file_ext not in allowed_extensions:
        raise ValueError(f"Invalid file type. Allowed: {', '.join(allowed_extensions)}")
    
    # Create unique filename
    unique_filename = f"project_{uuid4().hex[:8]}.{file_ext}"
    
    # Create upload directory
    upload_dir = os.path.join('app', 'static', 'images', 'projects')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_dir, unique_filename)
    image_file.save(file_path)
    
    # Return URL path
    url_path = f"/static/images/projects/{unique_filename}"
    print(f"Image saved successfully: {url_path}")
    return url_path

def save_base64_image(base64_data):
    """Convert base64 image to file"""
    try:
        # Parse base64 data
        header, data = base64_data.split(',', 1)
        image_data = base64.b64decode(data)
        
        # Determine file extension
        if 'jpeg' in header or 'jpg' in header:
            ext = 'jpg'
        elif 'png' in header:
            ext = 'png'
        elif 'gif' in header:
            ext = 'gif'
        elif 'webp' in header:
            ext = 'webp'
        else:
            ext = 'jpg'  # Default
        
        # Create unique filename
        filename = f"project_{uuid4().hex[:8]}.{ext}"
        
        # Create upload directory
        upload_dir = os.path.join('app', 'static', 'images', 'projects')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(image_data)
        
        # Return URL path
        url_path = f"/static/images/projects/{filename}"
        print(f"Base64 image converted and saved: {url_path}")
        return url_path
        
    except Exception as e:
        print(f"Error converting base64 image: {e}")
        raise ValueError("Failed to process base64 image data")

# MESSAGE MANAGEMENT
@admin_bp.route('/admin/messages')
def messages():
    """View messages with accurate statistics"""
    try:
        # Get all messages with proper ordering
        if hasattr(Message, 'get_all'):
            messages_list = Message.get_all()
        elif hasattr(Message, 'query'):
            messages_list = Message.query.order_by(Message.created_at.desc()).all()
        else:
            messages_list = []
        
        # Calculate accurate statistics
        total_messages = len(messages_list)
        unread_count = len([m for m in messages_list if hasattr(m, 'is_read') and not m.is_read])
        pending_count = len([m for m in messages_list if hasattr(m, 'status') and m.status == 'pending'])
        completed_count = len([m for m in messages_list if hasattr(m, 'status') and m.status == 'completed'])
        in_progress_count = len([m for m in messages_list if hasattr(m, 'status') and m.status == 'in-progress'])
        
        print(f"Messages statistics: Total={total_messages}, Unread={unread_count}, Pending={pending_count}")
        
        return render_template('admin/messages.html', 
                             messages=messages_list,
                             total_messages=total_messages,
                             unread_count=unread_count,
                             pending_count=pending_count,
                             completed_count=completed_count,
                             in_progress_count=in_progress_count)
    except Exception as e:
        print(f"Error loading messages: {str(e)}")
        flash(f'Error loading messages: {str(e)}', 'error')
        return render_template('admin/messages.html', 
                             messages=[],
                             total_messages=0,
                             unread_count=0,
                             pending_count=0,
                             completed_count=0,
                             in_progress_count=0)

@admin_bp.route('/admin/message/<int:message_id>')
def view_message(message_id):
    """View single message and mark as read"""
    try:
        message = Message.query.get_or_404(message_id)
        
        # Auto-mark as read when viewing
        if not message.is_read:
            message.is_read = True
            db.session.commit()
            print(f"Message {message_id} marked as read automatically")
        
        return render_template('admin/message_detail.html', message=message)
    except Exception as e:
        db.session.rollback()  # Add rollback in case of error
        flash(f'Error loading message: {str(e)}', 'error')
        return redirect(url_for('admin.messages'))

@admin_bp.route('/admin/message/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    """Delete message"""
    try:
        message = Message.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()
        flash('Message deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting message: {str(e)}', 'error')
    
    return redirect(url_for('admin.messages'))

# ADD THIS NEW ROUTE:
@admin_bp.route('/admin/message/update-status/<int:message_id>', methods=['POST'])
def update_message_status(message_id):
    """Update message status"""
    try:
        message = Message.query.get_or_404(message_id)
        new_status = request.form.get('status', '').strip()
        
        if new_status in ['pending', 'in-progress', 'completed', 'cancelled']:
            message.status = new_status
            
            # Mark as read when status is updated
            if not message.is_read:
                message.is_read = True
            
            db.session.commit()
            flash(f'Message status updated to "{new_status.title()}"!', 'success')
        else:
            flash('Invalid status value!', 'error')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating message status: {str(e)}', 'error')
    
    return redirect(url_for('admin.view_message', message_id=message_id))

# ADD THIS ROUTE FOR MARKING AS READ:
@admin_bp.route('/admin/message/mark-read/<int:message_id>', methods=['POST'])
def mark_message_read(message_id):
    """Mark message as read"""
    try:
        message = Message.query.get_or_404(message_id)
        message.is_read = True
        db.session.commit()
        flash('Message marked as read!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error marking message as read: {str(e)}', 'error')
    
    return redirect(url_for('admin.view_message', message_id=message_id))

# COMMENT MANAGEMENT
@admin_bp.route('/admin/comments')
def comments():
    """View comments with statistics"""
    try:
        # Get all comments
        comments_list = []
        if hasattr(Comment, 'get_all'):
            comments_list = Comment.get_all()
        elif hasattr(Comment, 'query'):
            comments_list = Comment.query.order_by(Comment.created_at.desc()).all()
        
        # Calculate statistics
        total_comments = len(comments_list)
        pending_count = len([c for c in comments_list if hasattr(c, 'is_approved') and not c.is_approved])
        approved_count = len([c for c in comments_list if hasattr(c, 'is_approved') and c.is_approved])
        
        print(f"Comments statistics: Total={total_comments}, Pending={pending_count}, Approved={approved_count}")
        
        return render_template('admin/comments.html', 
                             comments=comments_list,
                             total_comments=total_comments,
                             pending_count=pending_count,
                             approved_count=approved_count)
    except Exception as e:
        print(f"Error loading comments: {str(e)}")
        flash(f'Error loading comments: {str(e)}', 'error')
        return render_template('admin/comments.html', 
                             comments=[],
                             total_comments=0,
                             pending_count=0,
                             approved_count=0)

@admin_bp.route('/admin/comment/approve/<int:comment_id>', methods=['POST'])
def approve_comment(comment_id):
    """Approve comment"""
    try:
        comment = Comment.query.get_or_404(comment_id)
        comment.is_approved = True  # Fixed: use is_approved instead of approved
        db.session.commit()
        flash('Comment approved successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error approving comment: {str(e)}', 'error')
    
    return redirect(url_for('admin.comments'))

@admin_bp.route('/admin/comment/delete/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    """Delete comment"""
    try:
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting comment: {str(e)}', 'error')
    
    return redirect(url_for('admin.comments'))

# ADD THESE NEW BULK ACTION ROUTES:

@admin_bp.route('/admin/comments/bulk-approve', methods=['POST'])
def bulk_approve_comments():
    """Bulk approve comments"""
    try:
        comment_ids = request.form.getlist('comment_ids')
        if not comment_ids:
            flash('No comments selected for approval.', 'error')
            return redirect(url_for('admin.comments'))
        
        approved_count = 0
        for comment_id in comment_ids:
            try:
                comment = Comment.query.get(int(comment_id))
                if comment and not comment.is_approved:
                    comment.is_approved = True
                    approved_count += 1
            except (ValueError, TypeError):
                continue  # Skip invalid IDs
        
        db.session.commit()
        
        if approved_count > 0:
            flash(f'{approved_count} comment(s) approved successfully!', 'success')
        else:
            flash('No comments were approved.', 'info')
            
    except Exception as e:
        db.session.rollback()
        print(f"Error in bulk approve: {str(e)}")
        flash(f'Error approving comments: {str(e)}', 'error')
    
    return redirect(url_for('admin.comments'))

@admin_bp.route('/admin/comments/bulk-delete', methods=['POST'])
def bulk_delete_comments():
    """Bulk delete comments"""
    try:
        comment_ids = request.form.getlist('comment_ids')
        if not comment_ids:
            flash('No comments selected for deletion.', 'error')
            return redirect(url_for('admin.comments'))
        
        deleted_count = 0
        for comment_id in comment_ids:
            try:
                comment = Comment.query.get(int(comment_id))
                if comment:
                    db.session.delete(comment)
                    deleted_count += 1
            except (ValueError, TypeError):
                continue  # Skip invalid IDs
        
        db.session.commit()
        
        if deleted_count > 0:
            flash(f'{deleted_count} comment(s) deleted successfully!', 'success')
        else:
            flash('No comments were deleted.', 'info')
            
    except Exception as e:
        db.session.rollback()
        print(f"Error in bulk delete: {str(e)}")
        flash(f'Error deleting comments: {str(e)}', 'error')
    
    return redirect(url_for('admin.comments'))

# ADMIN USERS MANAGEMENT
@admin_bp.route('/admin/users')
def admin_users():
    """Display all admin users"""
    try:
        admin_users = AdminUser.query.all()
        return render_template('admin/admin_users.html', admin_users=admin_users)
    except Exception as e:
        print(f"Error fetching admin users: {str(e)}")
        flash(f'Error loading admin users: {str(e)}', 'error')
        return render_template('admin/admin_users.html', admin_users=[])

@admin_bp.route('/admin/user/add', methods=['GET', 'POST'])
def add_admin_user():
    """Add new admin user"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters long')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            errors.append('Invalid email format')
        
        # Check if username already exists
        existing_user = AdminUser.query.filter_by(username=username).first()
        if existing_user:
            errors.append('Username already exists')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/admin_user_form.html', 
                                 form_data=request.form, 
                                 action='add')
        
        try:
            # Create new admin user
            new_admin = AdminUser.create_admin(
                username=username,
                password=password,
                email=email if email else None,
                full_name=full_name if full_name else None
            )
            
            print(f"New admin user created: {username} by {session.get('admin_username')}")
            flash(f'Admin user "{username}" created successfully!', 'success')
            return redirect(url_for('admin.admin_users'))
            
        except Exception as e:
            print(f"Error creating admin user: {str(e)}")
            flash(f'Error creating admin user: {str(e)}', 'error')
            return render_template('admin/admin_user_form.html', 
                                 form_data=request.form, 
                                 action='add')
    
    return render_template('admin/admin_user_form.html', action='add')

@admin_bp.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_admin_user(user_id):
    """Edit admin user"""
    admin_user = AdminUser.query.get_or_404(user_id)
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        
        if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            errors.append('Invalid email format')
        
        # Check if username already exists (excluding current user)
        existing_user = AdminUser.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user_id:
            errors.append('Username already exists')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/admin_user_form.html', 
                                 admin_user=admin_user, 
                                 action='edit')
        
        try:
            # Update admin user
            admin_user.username = username
            admin_user.email = email if email else None
            admin_user.full_name = full_name if full_name else None
            admin_user.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            print(f"Admin user updated: {username} by {session.get('admin_username')}")
            flash(f'Admin user "{username}" updated successfully!', 'success')
            return redirect(url_for('admin.admin_users'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating admin user: {str(e)}")
            flash(f'Error updating admin user: {str(e)}', 'error')
    
    return render_template('admin/admin_user_form.html', 
                         admin_user=admin_user, 
                         action='edit')

@admin_bp.route('/admin/user/change-password/<int:user_id>', methods=['GET', 'POST'])
def change_admin_password(user_id):
    """Change admin user password"""
    admin_user = AdminUser.query.get_or_404(user_id)
    current_user_id = session.get('admin_user_id')
    is_own_password = (current_user_id == user_id)
    
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        errors = []
        
        # If changing own password, verify current password
        if is_own_password:
            if not current_password:
                errors.append('Current password is required')
            elif hasattr(admin_user, 'check_password') and not admin_user.check_password(current_password):
                errors.append('Current password is incorrect')
        
        if not new_password or len(new_password) < 6:
            errors.append('New password must be at least 6 characters long')
        
        if new_password != confirm_password:
            errors.append('New passwords do not match')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/change_password.html', 
                                 admin_user=admin_user, 
                                 is_own_password=is_own_password)
        
        try:
            # Update password
            if hasattr(admin_user, 'set_password'):
                admin_user.set_password(new_password)
            else:
                admin_user.password_hash = generate_password_hash(new_password)
            
            admin_user.updated_at = datetime.utcnow()
            
            # Reset login attempts if available
            if hasattr(admin_user, 'login_attempts'):
                admin_user.login_attempts = 0
            if hasattr(admin_user, 'locked_until'):
                admin_user.locked_until = None
            
            db.session.commit()
            
            action_by = session.get('admin_username')
            if is_own_password:
                print(f"Password changed by user: {admin_user.username}")
                flash('Your password has been changed successfully!', 'success')
            else:
                print(f"Password changed for {admin_user.username} by {action_by}")
                flash(f'Password changed for "{admin_user.username}" successfully!', 'success')
            
            return redirect(url_for('admin.admin_users'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error changing password: {str(e)}")
            flash(f'Error changing password: {str(e)}', 'error')
    
    return render_template('admin/change_password.html', 
                         admin_user=admin_user, 
                         is_own_password=is_own_password)

@admin_bp.route('/admin/user/toggle-lock/<int:user_id>', methods=['POST'])
def toggle_admin_lock(user_id):
    """Lock/unlock admin user account"""
    admin_user = AdminUser.query.get_or_404(user_id)
    current_user_id = session.get('admin_user_id')
    
    # Prevent locking own account
    if current_user_id == user_id:
        flash('You cannot lock your own account!', 'error')
        return redirect(url_for('admin.admin_users'))
    
    try:
        if hasattr(admin_user, 'is_locked') and admin_user.is_locked():
            # Unlock the account
            if hasattr(admin_user, 'locked_until'):
                admin_user.locked_until = None
            if hasattr(admin_user, 'login_attempts'):
                admin_user.login_attempts = 0
            action = 'unlocked'
        else:
            # Lock the account for 24 hours
            if hasattr(admin_user, 'locked_until'):
                admin_user.locked_until = datetime.utcnow() + timedelta(hours=24)
            action = 'locked'
        
        db.session.commit()
        
        print(f"Admin user {admin_user.username} {action} by {session.get('admin_username')}")
        flash(f'Admin user "{admin_user.username}" has been {action}!', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating account status: {str(e)}")
        flash(f'Error updating account status: {str(e)}', 'error')
    
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/user/delete/<int:user_id>', methods=['POST'])
def delete_admin_user(user_id):
    """Delete admin user"""
    admin_user = AdminUser.query.get_or_404(user_id)
    current_user_id = session.get('admin_user_id')
    
    # Prevent deleting own account
    if current_user_id == user_id:
        flash('You cannot delete your own account!', 'error')
        return redirect(url_for('admin.admin_users'))
    
    try:
        username = admin_user.username
        db.session.delete(admin_user)
        db.session.commit()
        
        print(f"Admin user {username} deleted by {session.get('admin_username')}")
        flash(f'Admin user "{username}" has been deleted!', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting admin user: {str(e)}")
        flash(f'Error deleting admin user: {str(e)}', 'error')
    
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/project/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    """Delete project"""
    try:
        project = Project.query.get_or_404(project_id)
        project_title = project.title
        
        db.session.delete(project)
        db.session.commit()
        
        flash(f'Project "{project_title}" deleted successfully!', 'success')
        print(f"Project {project_id} deleted: {project_title}")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting project: {str(e)}")
        flash(f'Error deleting project: {str(e)}', 'error')
    
    return redirect(url_for('admin.dashboard'))