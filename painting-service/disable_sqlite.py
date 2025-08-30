import os

def disable_sqlite_scripts():
    """Rename SQLite initialization scripts to prevent accidental use"""
    
    sqlite_scripts = [
        'init_db.py',
        'simple_init_db.py',
        'init_db_with_admin.py',
        'fix_database.py'
    ]
    
    print("🚫 Disabling SQLite initialization scripts...")
    
    for script in sqlite_scripts:
        if os.path.exists(script):
            new_name = f"{script}.disabled"
            os.rename(script, new_name)
            print(f"   🔄 Renamed: {script} → {new_name}")
        else:
            print(f"   ℹ️ Not found: {script}")
    
    print("✅ SQLite scripts disabled to prevent conflicts")

if __name__ == '__main__':
    disable_sqlite_scripts()