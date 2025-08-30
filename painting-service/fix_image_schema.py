import mysql.connector
from app import create_app, db

def fix_image_schema():
    """Fix image_url column to support long URLs"""
    
    print("🔧 Fixing image_url column schema...")
    
    try:
        # Direct MySQL update
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='GGTAHAEHt.1',
            database='color_and_craft'
        )
        
        cursor = connection.cursor()
        
        print("1️⃣ Updating image_url column to TEXT...")
        cursor.execute("ALTER TABLE projects MODIFY COLUMN image_url TEXT")
        connection.commit()
        
        print("2️⃣ Verifying change...")
        cursor.execute("DESCRIBE projects")
        columns = cursor.fetchall()
        
        for column in columns:
            if column[0] == 'image_url':
                print(f"   ✅ image_url column type: {column[1]}")
                break
        
        connection.close()
        
        print("✅ Schema updated successfully!")
        print("✅ Now supports:")
        print("   - Regular URLs")
        print("   - Base64 images")
        print("   - File uploads")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    fix_image_schema()