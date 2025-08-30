import mysql.connector
import getpass

def run_mysql_schema():
    """Run the MySQL schema as root user"""
    
    print("🚀 Running MySQL Schema Setup")
    print("=" * 40)
    
    # Get MySQL root password
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
        
        # Read and execute schema
        print("\n2️⃣ Reading mysql_schema.sql...")
        with open('mysql_schema.sql', 'r') as f:
            schema_content = f.read()
        
        # Split statements by semicolon and execute each
        statements = [stmt.strip() for stmt in schema_content.split(';') if stmt.strip()]
        
        print(f"\n3️⃣ Executing {len(statements)} SQL statements...")
        for i, statement in enumerate(statements, 1):
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    if i % 5 == 0:  # Progress indicator
                        print(f"   📊 Executed {i}/{len(statements)} statements...")
                except mysql.connector.Error as e:
                    if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                        continue  # Ignore duplicate/exists errors
                    else:
                        print(f"   ⚠️ Warning on statement {i}: {e}")
        
        print("   ✅ All statements executed!")
        
        # Commit changes
        connection.commit()
        
        # Test the setup
        print("\n4️⃣ Testing setup...")
        
        # Test user creation
        cursor.execute("SELECT User, Host FROM mysql.user WHERE User = 'color_and_craft'")
        user_result = cursor.fetchall()
        if user_result:
            print(f"   ✅ User 'color_and_craft' created successfully")
        else:
            print(f"   ❌ User creation failed")
        
        # Test database and tables
        cursor.execute("USE color_and_craft")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"   ✅ Database created with {len(tables)} tables:")
        for table in tables:
            print(f"      - {table[0]}")
        
        # Test admin user
        cursor.execute("SELECT username, email FROM admin_users")
        admin_users = cursor.fetchall()
        print(f"   ✅ Admin users: {len(admin_users)}")
        for admin in admin_users:
            print(f"      - {admin[0]} ({admin[1]})")
        
        # Test projects
        cursor.execute("SELECT COUNT(*) FROM projects")
        project_count = cursor.fetchone()[0]
        print(f"   ✅ Sample projects: {project_count}")
        
        connection.close()
        
        print("\n🎉 SUCCESS! Database setup complete!")
        print("=" * 40)
        print("✅ Database: color_and_craft")
        print("✅ User: color_and_craft")
        print("✅ Password: GGTAHAEHt.1")
        print("✅ Admin user: admin / admin123")
        print("✅ Email: Colour&craft@gmail.com")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ mysql_schema.sql file not found!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    run_mysql_schema()