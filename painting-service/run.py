from app import create_app
import os

# FORCE MySQL by removing any environment overrides
os.environ.pop('DATABASE_URL', None)

app = create_app()

# Debug route registration and database
print("\n🔍 Debug: Registered routes:")
for rule in app.url_map.iter_rules():
    if 'admin' in rule.rule or rule.rule == '/':
        print(f"  {rule.rule} -> {rule.endpoint}")

print(f"\n🔧 Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == "__main__":
    print("🚀 Starting Flask app with FORCED MySQL usage...")
    app.run(debug=True, host='0.0.0.0', port=5000)