from app import create_app

app = create_app()

print("🔍 Registered Admin Routes:")
for rule in app.url_map.iter_rules():
    if 'admin' in rule.rule.lower():
        print(f"  {rule.rule} -> {rule.endpoint}")

print("\n🔍 All Routes:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.rule} -> {rule.endpoint}")