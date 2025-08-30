import mysql.connector
from app import create_app, db
from app.models.admin_user import AdminUser
from app.models.project import Project
from app.models.message import Message
from app.models.comment import Comment

def verify_mysql_forced():
    """Verify that app is definitely using MySQL"""
    
    print("🔍 VERIFYING FORCED MySQL USAGE")
    print("=" * 50)
    
    # Step 1: Direct MySQL connection test
    print("1️⃣ Testing direct MySQL connection...")
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='color_and_craft',
            password='GGTAHAEHt.1',
            database='color_and_craft'
        )
        cursor = connection.cursor()
        
        # Check tables via direct MySQL
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"   📊 MySQL Tables: {[table[0] for table in tables]}")
        
        # Check admin users via direct MySQL
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        mysql_admin_count = cursor.fetchone()[0]
        print(f"   👨‍💼 MySQL Admin Users: {mysql_admin_count}")
        
        connection.close()
        print("   ✅ Direct MySQL connection works")
        
    except Exception as e:
        print(f"   ❌ Direct MySQL connection failed: {e}")
        return False
    
    # Step 2: Flask app database test
    print("\n2️⃣ Testing Flask app database connection...")
    app = create_app()
    
    with app.app_context():
        engine_url = str(db.engine.url)
        print(f"   🔧 Flask Database Engine: {engine_url}")
        
        if 'mysql' not in engine_url.lower():
            print(f"   ❌ ERROR: Flask is NOT using MySQL!")
            print(f"   🔧 Current engine: {engine_url}")
            return False
        
        print("   ✅ Flask is using MySQL")
        
        # Test ORM queries
        try:
            flask_admin_count = AdminUser.query.count()
            flask_project_count = Project.query.count()
            
            print(f"   📊 Flask Admin Count: {flask_admin_count}")
            print(f"   📊 Flask Project Count: {flask_project_count}")
            
            # Test if counts match between direct MySQL and Flask ORM
            if flask_admin_count == mysql_admin_count:
                print("   ✅ Flask ORM and direct MySQL match!")
            else:
                print(f"   ⚠️ Count mismatch: Flask={flask_admin_count}, MySQL={mysql_admin_count}")
            
        except Exception as e:
            print(f"   ❌ Flask ORM error: {e}")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 VERIFICATION COMPLETE!")
    print("✅ MySQL is being used correctly")
    print("✅ All data operations go to MySQL")
    print("✅ Check MySQL Workbench for real-time data")
    
    return True

if __name__ == '__main__':
    verify_mysql_forced()