from app import create_app, db
from app.models.admin_user import AdminUser

def check_admin_users():
    """Check admin users in database"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check admin users
            admin_users = AdminUser.query.all()
            print(f"👨‍💼 Admin Users in Database: {len(admin_users)}")
            
            if admin_users:
                for admin in admin_users:
                    print(f"  - ID: {admin.id}")
                    print(f"    Username: {admin.username}")
                    print(f"    Email: {admin.email}")
                    print(f"    Full Name: {admin.full_name}")
                    print(f"    Created: {admin.created_at}")
                    print(f"    Last Login: {admin.last_login}")
                    print("    " + "-" * 30)
            else:
                print("❌ No admin users found!")
                print("Creating default admin...")
                
                # Create default admin
                admin_user = AdminUser.create_admin(
                    username='admin',
                    password='admin123',
                    email='Colour&craft@gmail.com',
                    full_name='Administrator'
                )
                print(f"✅ Created admin: {admin_user.username}")
                
        except Exception as e:
            print(f"❌ Error checking admin users: {e}")
            print(f"Error details: {str(e)}")

if __name__ == '__main__':
    check_admin_users()