from app import create_app, db
from app.models.admin_user import AdminUser

def ensure_admin_exists():
    """Ensure default admin user exists"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if admin exists
            admin_user = AdminUser.query.filter_by(username='admin').first()
            
            if admin_user:
                print(f"✅ Admin user exists: {admin_user.username}")
                print(f"   Email: {admin_user.email}")
                print(f"   Created: {admin_user.created_at}")
                
                # Test authentication
                auth_user, message = AdminUser.authenticate('admin', 'admin123')
                if auth_user:
                    print(f"✅ Authentication test passed")
                else:
                    print(f"❌ Authentication test failed: {message}")
                    
            else:
                print("❌ No admin user found. Creating...")
                
                # Create admin user
                admin_user = AdminUser.create_admin(
                    username='admin',
                    password='admin123',
                    email='Colour&craft@gmail.com',
                    full_name='Administrator'
                )
                
                print(f"✅ Admin user created!")
                print(f"   Username: admin")
                print(f"   Password: admin123")
                print(f"   Email: Colour&craft@gmail.com")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    ensure_admin_exists()