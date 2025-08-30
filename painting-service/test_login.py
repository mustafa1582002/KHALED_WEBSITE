from app import create_app
from flask import session

def test_login():
    app = create_app()
    
    with app.test_client() as client:
        # Test login with correct credentials
        print("Testing login with correct credentials:")
        response = client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        
        print(f"Response status: {response.status_code}")
        print(f"Response location: {response.location}")
        print(f"Session data: {session}")
        
        # Print response data
        html = response.data.decode('utf-8')
        if "Welcome to the admin panel" in html:
            print("✅ Login successful - found welcome message")
        else:
            print("❌ Login failed - welcome message not found")
            
        if "Admin Dashboard" in html:
            print("✅ Dashboard loaded successfully")
        else:
            print("❌ Dashboard failed to load")

if __name__ == '__main__':
    test_login()