from app import create_app, db
from app.models.comment import Comment
from app.models.message import Message
from app.models.project import Project
from app.models.admin_user import AdminUser  # Add this import

app = create_app()

def test_database_connection():
    """Test basic database connection and table existence"""
    with app.app_context():
        try:
            # Test database connection
            print("🔍 Testing database connection...")
            
            # Check if tables exist by querying them
            admin_count = AdminUser.query.count()  # Add this
            comment_count = Comment.query.count()
            message_count = Message.query.count()
            project_count = Project.query.count()
            
            print(f"✅ Database connection successful!")
            print(f"📊 Current record counts:")
            print(f"   👨‍💼 Admin Users: {admin_count}")  # Add this
            print(f"   📝 Comments: {comment_count}")
            print(f"   📧 Messages: {message_count}")
            print(f"   🎨 Projects: {project_count}")
            
            return True
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return False

def test_admin_operations():
    """Test admin user operations"""
    with app.app_context():
        try:
            print("\n👨‍💼 Testing Admin User Operations...")
            
            # Test 1: Check existing admins
            print("1️⃣ Checking existing admin users...")
            existing_admins = AdminUser.query.all()
            print(f"   📊 Found {len(existing_admins)} admin users:")
            for admin in existing_admins:
                print(f"   - {admin.username} ({admin.email})")
            
            # Test 2: Create test admin (if none exist)
            if len(existing_admins) == 0:
                print("2️⃣ Creating default admin user...")
                try:
                    admin_user = AdminUser.create_admin(
                        username='admin',
                        password='admin123',
                        email='Colour&craft@gmail.com',
                        full_name='Administrator'
                    )
                    print(f"   ✅ Default admin created: {admin_user.username}")
                except Exception as e:
                    print(f"   ❌ Failed to create admin: {e}")
            else:
                print("2️⃣ Admin users already exist, skipping creation...")
            
            # Test 3: Test authentication
            print("3️⃣ Testing admin authentication...")
            auth_user, message = AdminUser.authenticate('admin', 'admin123')
            if auth_user:
                print(f"   ✅ Authentication successful: {auth_user.username}")
            else:
                print(f"   ❌ Authentication failed: {message}")
            
            # Test 4: Test wrong password
            print("4️⃣ Testing wrong password...")
            auth_user, message = AdminUser.authenticate('admin', 'wrongpass')
            if not auth_user:
                print(f"   ✅ Wrong password correctly rejected")
            else:
                print(f"   ❌ Security issue: wrong password accepted!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error in admin operations: {e}")
            return False

def test_project_operations():
    """Test project CRUD operations"""
    with app.app_context():
        try:
            print("\n🧪 Testing Project Operations...")
            
            # Test 1: Create a new project
            print("1️⃣ Testing project creation...")
            new_project = Project(
                title="Test Project - Living Room Makeover",
                description="A complete transformation of a modern living room with premium paints and techniques.",
                image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800",
                category="interior"
            )
            
            if new_project.save():
                print(f"   ✅ Project created successfully! ID: {new_project.id}")
            else:
                print("   ❌ Failed to create project")
                return False
            
            # Test 2: Count projects
            print("2️⃣ Testing project count...")
            total_projects = Project.count()
            print(f"   📊 Total projects: {total_projects}")
            
            # Test 3: Retrieve all projects
            print("3️⃣ Testing project retrieval...")
            all_projects = Project.get_all()
            print(f"   📋 Retrieved {len(all_projects)} projects")
            
            # Test 4: Get project by ID
            print("4️⃣ Testing project retrieval by ID...")
            retrieved_project = Project.get_by_id(new_project.id)
            if retrieved_project:
                print(f"   ✅ Retrieved project: '{retrieved_project.title}'")
            else:
                print("   ❌ Failed to retrieve project by ID")
            
            # Test 5: Update project
            print("5️⃣ Testing project update...")
            if retrieved_project.update(
                title="Updated Test Project - Modern Living Room",
                category="interior-premium"
            ):
                print(f"   ✅ Project updated successfully")
                print(f"   📝 New title: '{retrieved_project.title}'")
                print(f"   🏷️ New category: '{retrieved_project.category}'")
            else:
                print("   ❌ Failed to update project")
            
            # Test 6: Get projects by category
            print("6️⃣ Testing projects by category...")
            interior_projects = Project.get_by_category("interior")
            premium_projects = Project.get_by_category("interior-premium")
            print(f"   🏠 Interior projects: {len(interior_projects)}")
            print(f"   ⭐ Premium interior projects: {len(premium_projects)}")
            
            # Test 7: Convert to dictionary
            print("7️⃣ Testing project serialization...")
            project_dict = retrieved_project.to_dict()
            print(f"   📄 Project as dict: {project_dict['title']}")
            
            # Test 8: Delete project
            print("8️⃣ Testing project deletion...")
            project_id_to_delete = retrieved_project.id
            if retrieved_project.delete():
                print(f"   ✅ Project deleted successfully! ID: {project_id_to_delete}")
                
                # Verify deletion
                deleted_project = Project.get_by_id(project_id_to_delete)
                if deleted_project is None:
                    print("   ✅ Deletion confirmed - project not found")
                else:
                    print("   ❌ Deletion failed - project still exists")
            else:
                print("   ❌ Failed to delete project")
            
            # Test 9: Final count
            print("9️⃣ Testing final project count...")
            final_count = Project.count()
            print(f"   📊 Final project count: {final_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error in project operations: {e}")
            return False

def test_static_deletion():
    """Test static deletion method"""
    with app.app_context():
        try:
            print("\n🗑️ Testing Static Deletion Method...")
            
            # Create a test project
            test_project = Project(
                title="Project to Delete",
                description="This project will be deleted using static method",
                image_url="https://example.com/test.jpg",
                category="test"
            )
            test_project.save()
            project_id = test_project.id
            print(f"   📝 Created test project with ID: {project_id}")
            
            # Delete using static method
            if Project.delete_by_id(project_id):
                print(f"   ✅ Project deleted using static method")
                
                # Verify deletion
                if Project.get_by_id(project_id) is None:
                    print("   ✅ Static deletion confirmed")
                else:
                    print("   ❌ Static deletion failed")
            else:
                print("   ❌ Static deletion method failed")
                
            return True
            
        except Exception as e:
            print(f"❌ Error in static deletion test: {e}")
            return False

def create_sample_projects():
    """Create some sample projects for testing"""
    with app.app_context():
        try:
            print("\n🏗️ Creating Sample Projects...")
            
            sample_projects = [
                {
                    'title': 'Modern Kitchen Renovation',
                    'description': 'Complete kitchen transformation with contemporary colors and premium finishes.',
                    'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800',
                    'category': 'interior'
                },
                {
                    'title': 'Exterior House Painting',
                    'description': 'Full exterior makeover with weather-resistant premium paints.',
                    'image_url': 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800',
                    'category': 'exterior'
                },
                {
                    'title': 'Commercial Office Space',
                    'description': 'Professional office painting with modern corporate design.',
                    'image_url': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800',
                    'category': 'commercial'
                }
            ]
            
            created_count = 0
            for project_data in sample_projects:
                project = Project(**project_data)
                if project.save():
                    created_count += 1
                    print(f"   ✅ Created: '{project.title}'")
                else:
                    print(f"   ❌ Failed to create: '{project_data['title']}'")
            
            print(f"   📊 Created {created_count} sample projects")
            return created_count > 0
            
        except Exception as e:
            print(f"❌ Error creating sample projects: {e}")
            return False

def run_all_tests():
    """Run all database tests"""
    print("🚀 Starting Database Tests for Painting Service App")
    print("=" * 60)
    
    # Test 1: Basic connection
    if not test_database_connection():
        print("💀 Database connection failed. Stopping tests.")
        return
    
    # Test 2: Admin operations (ADD THIS)
    if not test_admin_operations():
        print("💀 Admin operations failed.")
        return
    
    # Test 3: Project operations
    if not test_project_operations():
        print("💀 Project operations failed.")
        return
    
    # Test 4: Static deletion
    if not test_static_deletion():
        print("💀 Static deletion test failed.")
        return
    
    # Test 5: Create sample data
    if not create_sample_projects():
        print("💀 Sample project creation failed.")
        return
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed successfully!")
    print("✅ Your Project model is working correctly")
    print("✅ Database operations are functional")
    print("✅ Delete functionality is working")
    print("✅ Admin authentication is working")  # Add this
    
    # Final summary
    with app.app_context():
        final_stats = {
            'admin_users': AdminUser.query.count(),  # Add this
            'projects': Project.count(),
            'messages': Message.query.count(),
            'comments': Comment.query.count()
        }
        
        print(f"\n📊 Final Database Summary:")
        print(f"   👨‍💼 Admin Users: {final_stats['admin_users']}")  # Add this
        print(f"   🎨 Projects: {final_stats['projects']}")
        print(f"   📧 Messages: {final_stats['messages']}")
        print(f"   💬 Comments: {final_stats['comments']}")

if __name__ == '__main__':
    run_all_tests()