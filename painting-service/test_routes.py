from app import create_app

app = create_app()

print("🔍 Checking for secure admin access route:")
found = False
for rule in app.url_map.iter_rules():
    if 'secure-admin-access' in rule.rule:
        print(f"✅ Found: {rule.rule} -> {rule.endpoint}")
        found = True

if not found:
    print("❌ Secure admin access route not found!")
    
print("\n🔍 All admin routes:")
for rule in app.url_map.iter_rules():
    if 'admin' in rule.rule.lower():
        print(f"  {rule.rule} -> {rule.endpoint}")