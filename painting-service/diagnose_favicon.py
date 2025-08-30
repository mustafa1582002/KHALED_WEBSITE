import os
from app import create_app

def diagnose_favicon():
    """Diagnose favicon issues"""
    
    print("🔍 Diagnosing favicon setup...")
    
    # 1. Check files exist
    favicon_dir = os.path.join('app', 'static', 'favicon')
    files = ['favicon.ico', 'favicon-16x16.png', 'favicon-32x32.png', 'apple-touch-icon.png']
    
    print("\n1️⃣ File existence check:")
    for file in files:
        path = os.path.join(favicon_dir, file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"   ✅ {file} ({size} bytes)")
        else:
            print(f"   ❌ {file} - MISSING")
    
    # 2. Test Flask routes
    print("\n2️⃣ Testing Flask routes...")
    app = create_app()
    
    with app.test_client() as client:
        # Test static file access
        response = client.get('/static/favicon/favicon.ico')
        print(f"   /static/favicon/favicon.ico: {response.status_code}")
        
        response = client.get('/favicon.ico')
        print(f"   /favicon.ico: {response.status_code}")
        
        # Test a page to see if favicon links are rendered
        response = client.get('/')
        if response.status_code == 200:
            content = response.get_data(as_text=True)
            if 'favicon/favicon.ico' in content:
                print(f"   ✅ Favicon links found in home page HTML")
            else:
                print(f"   ❌ Favicon links NOT found in home page HTML")
        else:
            print(f"   ❌ Home page returned {response.status_code}")
    
    # 3. Test with running server
    print("\n3️⃣ Testing with running server...")
    print("   Start your Flask app with 'python run.py' and then:")
    print("   Check: http://localhost:5000/static/favicon/favicon.ico")
    print("   Check: http://localhost:5000/favicon.ico")
    
    print("\n✅ Diagnosis complete!")

if __name__ == '__main__':
    diagnose_favicon()