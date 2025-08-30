from app import create_app, db
from app.models.admin_user import AdminUser
from app.models.project import Project
from app.models.message import Message
from app.models.comment import Comment
import mysql.connector
import os

def force_mysql_initialization():
    """Force complete MySQL initialization - delete any SQLite files"""
    
    print("🚀 FORCING MySQL Usage - Complete Initialization")
    print("=" * 60)
    
    # Step 1: Delete any SQLite files
    print("1️⃣ Removing any SQLite databases...")
    sqlite_files = [
        'painting_service.db',
        'instance/painting_service.db',
        'app.db',
        'database.db'
    ]
    
    for db_file in sqlite_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"   🗑️ Deleted: {db_file}")
    
    # Remove instance directory if exists
    if os.path.exists('instance'):
        import shutil
        shutil.rmtree('instance')
        print(f"   🗑️ Deleted: instance/ directory")
    
    # Step 2: Verify MySQL connection with CORRECT credentials
    print("\n2️⃣ Testing MySQL connection...")
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # CORRECT username
            password='GGTAHAEHt.1',
            database='color_and_craft'
        )
        connection.close()
        print("   ✅ MySQL connection successful!")
    except Exception as e:
        print(f"   ❌ MySQL connection failed: {e}")
        print("   🔧 Make sure MySQL is running and credentials are correct")
        return False
    
    # Step 3: Force app to use MySQL
    print("\n3️⃣ Creating Flask app with FORCED MySQL...")
    
    # Force environment to prevent any SQLite fallback
    os.environ.pop('DATABASE_URL', None)  # Remove any environment override
    
    app = create_app()
    
    with app.app_context():
        print(f"   📊 App Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Verify we're connected to MySQL, not SQLite
        engine_url = str(db.engine.url)
        if 'mysql' not in engine_url:
            print(f"   ❌ ERROR: Still using {engine_url}")
            return False
        else:
            print(f"   ✅ Confirmed MySQL usage: {engine_url}")
        
        # Step 4: Drop and recreate all tables
        print("\n4️⃣ Recreating MySQL tables...")
        db.drop_all()
        print("   🗑️ Dropped all existing tables")
        
        db.create_all()
        print("   🏗️ Created all tables fresh")
        
        # Step 5: Create admin user
        print("\n5️⃣ Creating admin user...")
        try:
            # Check if admin already exists
            existing_admin = AdminUser.query.filter_by(username='admin').first()
            if existing_admin:
                print("   ℹ️ Admin user already exists, skipping creation")
            else:
                admin_user = AdminUser.create_admin(
                    username='admin',
                    password='admin123',
                    email='Colour&craft@gmail.com',
                    full_name='Administrator'
                )
                print(f"   ✅ Admin user created: {admin_user.username}")
        except Exception as e:
            print(f"   ❌ Error creating admin: {e}")
            return False
        
        # Step 6: Verify everything is in MySQL
        print("\n6️⃣ Verifying data in MySQL...")
        try:
            admin_count = AdminUser.query.count()
            project_count = Project.query.count()
            message_count = Message.query.count()
            comment_count = Comment.query.count()
            
            print(f"   📊 Admin Users: {admin_count}")
            print(f"   📊 Projects: {project_count}")
            print(f"   📊 Messages: {message_count}")
            print(f"   📊 Comments: {comment_count}")
            
        except Exception as e:
            print(f"   ❌ Error verifying data: {e}")
            return False
    
    print("\n" + "=" * 60)
    print("🎉 SUCCESS: MySQL forced initialization complete!")
    print("✅ All data will now be stored in MySQL")
    print("✅ No more SQLite files")
    print("✅ Check MySQL Workbench to see your data")
    print("\n🔐 Admin Login:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   URL: http://localhost:5000/secure-admin-access/color-craft-admin-2024")
    
    return True

if __name__ == '__main__':
    force_mysql_initialization()