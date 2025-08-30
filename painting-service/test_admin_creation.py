from app import create_app, db
from app.models.admin_user import AdminUser
from app.models.project import Project
from flask import render_template, flash, Blueprint

# Create blueprint for admin routes
admin_bp = Blueprint('admin', __name__)

def test_admin_creation():
    """Test admin user creation and authentication"""
    app = create_app()
    
    with app.app_context():
        # Test creating a new admin
        test_username = "testadmin"
        test_password = "testpass123"
        
        print(f"🧪 Testing admin creation...")
        
        # Delete test user if exists
        existing = AdminUser.query.filter_by(username=test_username).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            print(f"  Deleted existing test user")
        
        # Create test admin
        try:
            test_admin = AdminUser.create_admin(
                username=test_username,
                password=test_password,
                email="test@example.com",
                full_name="Test Administrator"
            )
            print(f"✅ Test admin created: {test_username}")
            
            # Test authentication
            auth_user, message = AdminUser.authenticate(test_username, test_password)
            if auth_user:
                print(f"✅ Authentication successful: {message}")
            else:
                print(f"❌ Authentication failed: {message}")
            
            # Test wrong password
            auth_user, message = AdminUser.authenticate(test_username, "wrongpass")
            if not auth_user:
                print(f"✅ Wrong password correctly rejected: {message}")
            else:
                print(f"❌ Wrong password incorrectly accepted")
            
            # Clean up
            db.session.delete(test_admin)
            db.session.commit()
            print(f"🧹 Test user cleaned up")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
        
        # List current admins
        all_admins = AdminUser.query.all()
        print(f"\n📋 All admin users:")
        for admin in all_admins:
            print(f"  - ID: {admin.id}, Username: {admin.username}, Email: {admin.email}")

@admin_bp.route('/admin/dashboard')
def dashboard():
    """Admin dashboard"""
    print("Dashboard route accessed")
    
    try:
        # Get projects
        projects = []
        if hasattr(Project, 'get_all'):
            projects = Project.get_all()
        elif hasattr(Project, 'query'):
            projects = Project.query.all()
        
        # Get admin users count
        admin_users_count = 0
        try:
            admin_users_count = AdminUser.query.count()
        except Exception as e:
            print(f"Error counting admin users: {str(e)}")
        
        print(f"Dashboard data: {len(projects)} projects, {admin_users_count} admin users")
        
        return render_template('admin/dashboard.html', 
                             projects=projects,
                             admin_users_count=admin_users_count)
    except Exception as e:
        print(f"Error in dashboard: {str(e)}")
        flash(f'Dashboard error: {str(e)}', 'error')
        return render_template('admin/dashboard.html', projects=[], admin_users_count=0)

if __name__ == '__main__':
    test_admin_creation()