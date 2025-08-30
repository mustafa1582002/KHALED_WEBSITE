from app import create_app, db
from app.models.admin_user import AdminUser

def init_admin():
    """Initialize default admin user"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if default admin exists
        admin_user = AdminUser.query.filter_by(username='admin').first()
        
        if not admin_user:
            # Create default admin user
            admin_user = AdminUser.create_admin(
                username='admin',
                password='admin123',
                email='Colour&craft@gmail.com',  # Updated email
                full_name='Administrator'
            )
            print("✅ Default admin user created:")
            print(f"  Username: admin")
            print(f"  Password: admin123")
        else:
            print("✅ Default admin user already exists")
        
        # List all admin users
        all_admins = AdminUser.query.all()
        print(f"\n📋 Current admin users ({len(all_admins)}):")
        for admin in all_admins:
            print(f"  - {admin.username} ({admin.email or 'no email'})")
        
        print("✅ Database initialized successfully!")

if __name__ == '__main__':
    init_admin()