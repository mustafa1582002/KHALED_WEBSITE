import sqlite3
import os
from app import create_app, db

def update_database():
    """Add missing category column to projects table"""
    
    # Get the database path
    instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
    db_path = os.path.join(instance_dir, 'painting_service.db')
    
    if not os.path.exists(db_path):
        print("Database file not found. Creating new database...")
        app = create_app()
        with app.app_context():
            db.create_all()
        print("New database created successfully!")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if category column exists
        cursor.execute("PRAGMA table_info(projects)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'category' not in columns:
            print("Adding 'category' column to projects table...")
            cursor.execute("ALTER TABLE projects ADD COLUMN category VARCHAR(50) DEFAULT 'general'")
            conn.commit()
            print("✅ Category column added successfully!")
        else:
            print("✅ Category column already exists!")
            
        # Verify the update
        cursor.execute("PRAGMA table_info(projects)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"Current columns in projects table: {columns}")
        
    except Exception as e:
        print(f"❌ Error updating database: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    update_database()