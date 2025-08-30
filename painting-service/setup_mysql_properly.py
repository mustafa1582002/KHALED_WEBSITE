import mysql.connector
import sys
import getpass

def setup_mysql_properly():
    """Set up MySQL database and user properly"""
    
    print("🚀 MySQL Database & User Setup")
    print("=" * 40)
    
    # Get root password from user
    print("Enter your MySQL root password (press Enter if no password):")
    root_password = getpass.getpass("Root password: ")
    
    try:
        # Connect as root
        print("\n1️⃣ Connecting to MySQL as root...")
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=root_password
        )
        cursor = connection.cursor()
        print("   ✅ Connected successfully!")
        
        # Create database
        print("\n2️⃣ Creating database...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS color_and_craft")
        print("   ✅ Database 'color_and_craft' created/verified")
        
        # Create user
        print("\n3️⃣ Creating user...")
        try:
            cursor.execute("DROP USER IF EXISTS 'color_and_craft'@'localhost'")
            cursor.execute("CREATE USER 'color_and_craft'@'localhost' IDENTIFIED BY 'GGTAHAEHt.1'")
            print("   ✅ User 'color_and_craft' created")
        except mysql.connector.Error as e:
            print(f"   ⚠️ User creation warning: {e}")
        
        # Grant privileges
        print("\n4️⃣ Granting privileges...")
        cursor.execute("GRANT ALL PRIVILEGES ON color_and_craft.* TO 'color_and_craft'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        print("   ✅ Privileges granted")
        
        # Run your schema
        print("\n5️⃣ Setting up tables...")
        cursor.execute("USE color_and_craft")
        
        # Read and execute your schema
        with open('mysql_schema.sql', 'r') as f:
            schema_content = f.read()
        
        # Split and execute each statement
        statements = schema_content.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except mysql.connector.Error as e:
                    if "already exists" in str(e) or "Duplicate" in str(e):
                        continue  # Ignore duplicate errors
                    print(f"   ⚠️ Statement warning: {e}")
        
        print("   ✅ Schema applied successfully")
        
        # Test the new user
        print("\n6️⃣ Testing new user connection...")
        connection.close()
        
        test_connection = mysql.connector.connect(
            host='localhost',
            user='color_and_craft',
            password='GGTAHAEHt.1',
            database='color_and_craft'
        )
        
        test_cursor = test_connection.cursor()
        test_cursor.execute("SHOW TABLES")
        tables = test_cursor.fetchall()
        
        print(f"   ✅ New user works! Found {len(tables)} tables:")
        for table in tables:
            print(f"      - {table[0]}")
        
        # Check admin user
        test_cursor.execute("SELECT COUNT(*) FROM admin_users")
        admin_count = test_cursor.fetchone()[0]
        print(f"   📊 Admin users: {admin_count}")
        
        test_connection.close()
        
        print("\n🎉 SUCCESS! MySQL is properly configured!")
        print("=" * 40)
        print("✅ Database: color_and_craft")
        print("✅ User: color_and_craft")
        print("✅ Password: GGTAHAEHt.1")
        print("✅ All tables created")
        print("✅ Admin user ready")
        
        print(f"\n🔧 Update your config.py with:")
        print(f"SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://color_and_craft:GGTAHAEHt.1@localhost/color_and_craft'")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    setup_mysql_properly()