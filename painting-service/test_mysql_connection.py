import mysql.connector

def test_mysql_connection():
    """Test MySQL connection with the correct user"""
    
    print("🧪 Testing MySQL Connection")
    print("=" * 30)
    
    try:
        # CORRECT connection details
        print("1️⃣ Testing root user...")
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # CORRECT username
            password='GGTAHAEHt.1',
            database='color_and_craft'
        )
        
        cursor = connection.cursor()
        
        # Test queries
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        admin_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM projects")
        project_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT username, email FROM admin_users WHERE username = 'admin'")
        admin_info = cursor.fetchone()
        
        print(f"   ✅ Connection successful!")
        print(f"   📊 Admin users: {admin_count}")
        print(f"   📊 Projects: {project_count}")
        if admin_info:
            print(f"   👤 Default admin: {admin_info[0]} ({admin_info[1]})")
        
        connection.close()
        
        print("\n🎉 MySQL is ready for Flask app!")
        print("✅ Update your config.py with:")
        print("   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:GGTAHAEHt.1@localhost/color_and_craft'")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"   ❌ Connection failed: {e}")
        return False

if __name__ == '__main__':
    test_mysql_connection()