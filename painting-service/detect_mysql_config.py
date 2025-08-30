import mysql.connector
import sys

def detect_mysql_config():
    """Detect working MySQL configuration"""
    
    print("🔍 DETECTING MySQL Configuration...")
    print("=" * 50)
    
    # Test different configurations
    test_configs = [
        {
            'name': 'Root User (most common)',
            'host': 'localhost',
            'user': 'root',
            'password': '',  # Empty password
            'database': 'color_and_craft'
        },
        {
            'name': 'Root User with common passwords',
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'database': 'color_and_craft'
        },
        {
            'name': 'Root User with password',
            'host': 'localhost',
            'user': 'root',
            'password': 'password',
            'database': 'color_and_craft'
        },
        {
            'name': 'Current color_and_craft user',
            'host': 'localhost',
            'user': 'color_and_craft',
            'password': 'GGTAHAEHt.1',
            'database': 'color_and_craft'
        }
    ]
    
    working_config = None
    
    for config in test_configs:
        print(f"\n🧪 Testing: {config['name']}")
        print(f"   User: {config['user']}")
        print(f"   Password: {'*' * len(config['password']) if config['password'] else '(empty)'}")
        
        try:
            connection = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password']
            )
            
            print(f"   ✅ Connection successful!")
            
            # Check if database exists
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES LIKE 'color_and_craft'")
            db_exists = cursor.fetchone() is not None
            
            if db_exists:
                print(f"   ✅ Database 'color_and_craft' exists!")
                
                # Test accessing the database
                cursor.execute("USE color_and_craft")
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"   📊 Tables found: {len(tables)}")
                
                working_config = config
                connection.close()
                break
            else:
                print(f"   ⚠️ Database 'color_and_craft' not found")
                connection.close()
                
        except mysql.connector.Error as e:
            print(f"   ❌ Connection failed: {e}")
    
    if working_config:
        print(f"\n🎉 WORKING CONFIGURATION FOUND!")
        print("=" * 50)
        print(f"✅ Use this in your config.py:")
        print(f"SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{working_config['user']}:{working_config['password']}@{working_config['host']}/{working_config['database']}'")
        return working_config
    else:
        print(f"\n❌ NO WORKING CONFIGURATION FOUND!")
        print("🔧 You need to:")
        print("1. Make sure MySQL is running")
        print("2. Create the database and user")
        print("3. Check your MySQL root password")
        return None

if __name__ == '__main__':
    detect_mysql_config()