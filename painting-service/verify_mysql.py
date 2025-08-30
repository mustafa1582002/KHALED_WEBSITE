import mysql.connector
from config import Config

def verify_mysql_setup():
    """Verify MySQL database is set up correctly"""
    connection = None
    try:
        # CORRECT connection details
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Changed to root
            password='GGTAHAEHt.1',
            database='color_and_craft'
        )
        
        cursor = connection.cursor()
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("✅ Database tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Check admin user
        cursor.execute("SELECT username, email FROM admin_users")
        admin_users = cursor.fetchall()
        print("\n✅ Admin users:")
        for user in admin_users:
            print(f"   - {user[0]} ({user[1]})")
        
        # Check indexes
        cursor.execute("SHOW INDEXES FROM admin_users")
        indexes = cursor.fetchall()
        print(f"\n✅ Admin users indexes: {len(indexes)} found")
        
        print("\n🎉 MySQL database is properly configured!")
        
    except Exception as e:
        print(f"❌ MySQL connection error: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    verify_mysql_setup()