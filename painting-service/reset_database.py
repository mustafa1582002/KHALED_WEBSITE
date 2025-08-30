import os
from app import create_app, db
from app.models.admin_user import AdminUser
from app.models.project import Project
from app.models.message import Message
from app.models.comment import Comment

def reset_database():
    """Delete and recreate the database with correct schema"""
    
    # Delete existing database files
    db_files = [
        'instance/painting_service.db',
        'app/painting_service.db'
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"Deleted {db_file}")
    
    # Create fresh database
    app = create_app()
    with app.app_context():
        print("Creating new database with correct schema...")
        db.create_all()
        
        # Create admin user
        admin_user = AdminUser.create_admin(
            username='admin',
            password='admin123',
            email='admin@colorcraft.com',
            full_name='Administrator'
        )
        
        # Create sample project
        sample_project = Project(
            title="Modern Kitchen Renovation",
            description="A beautiful modern kitchen with contemporary colors.",
            image_url="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800",
            category="interior"
        )
        sample_project.save()
        
        # Create sample comment with all fields
        sample_comment = Comment(
            name="John Doe",
            email="john@example.com",
            content="Amazing work! Professional service.",
            client_type="homeowner",
            project_id=sample_project.id,
            rating=5
        )
        sample_comment.is_approved = True
        sample_comment.save()
        
        print("✅ Database reset complete!")
        print("Login credentials: admin / admin123")

if __name__ == '__main__':
    reset_database()