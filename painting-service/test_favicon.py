import os

def test_favicon_files():
    """Test if favicon files exist and are accessible"""
    
    print("🔍 Testing favicon files...")
    
    favicon_dir = os.path.join('app', 'static', 'favicon')
    required_files = [
        'favicon.ico',
        'favicon-16x16.png',
        'favicon-32x32.png',
        'apple-touch-icon.png',
        'site.webmanifest'
    ]
    
    print(f"📂 Checking directory: {favicon_dir}")
    
    if not os.path.exists(favicon_dir):
        print(f"❌ Directory doesn't exist: {favicon_dir}")
        return False
    
    all_exist = True
    for filename in required_files:
        filepath = os.path.join(favicon_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"   ✅ {filename} ({size} bytes)")
        else:
            print(f"   ❌ Missing: {filename}")
            all_exist = False
    
    if all_exist:
        print("\n🎉 All favicon files are present!")
        print("\n🔗 URLs that should work:")
        print("   http://localhost:5000/static/favicon/favicon.ico")
        print("   http://localhost:5000/static/favicon/favicon-32x32.png")
    else:
        print("\n❌ Some favicon files are missing!")
    
    return all_exist

if __name__ == '__main__':
    test_favicon_files()