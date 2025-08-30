import mysql.connector
from app import create_app, db
from app.models.project import Project

def check_projects():
    """Check if projects exist in database"""
    
    print("🔍 Checking projects in database...")
    
    # Method 1: Direct MySQL check
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='GGTAHAEHt.1',
            database='color_and_craft'
        )
        
        cursor = connection.cursor()
        
        print("\n1️⃣ Direct database check:")
        cursor.execute("SELECT COUNT(*) FROM projects")
        db_count = cursor.fetchone()[0]
        print(f"   Total projects in database: {db_count}")
        
        if db_count > 0:
            cursor.execute("SELECT id, title, category, created_at FROM projects ORDER BY created_at DESC")
            projects = cursor.fetchall()
            print(f"   Projects found:")
            for project in projects:
                print(f"     ID: {project[0]}, Title: {project[1]}, Category: {project[2]}, Created: {project[3]}")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")
    
    # Method 2: Flask app check
    try:
        print("\n2️⃣ Flask app check:")
        app = create_app()
        
        with app.app_context():
            flask_count = Project.query.count()
            print(f"   Projects via Flask: {flask_count}")
            
            if flask_count > 0:
                projects = Project.query.all()
                print(f"   Flask projects:")
                for project in projects:
                    print(f"     ID: {project.id}, Title: {project.title}")
            
            # Test the get_all method if it exists
            if hasattr(Project, 'get_all'):
                get_all_projects = Project.get_all()
                print(f"   Projects via get_all(): {len(get_all_projects)}")
            
    except Exception as e:
        print(f"❌ Flask check failed: {e}")
    
    print("\n✅ Check complete!")

if __name__ == '__main__':
    check_projects()