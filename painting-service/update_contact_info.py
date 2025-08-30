import os
import re

def update_contact_info():
    """Update all email and phone references"""
    
    # Define the mappings
    email_patterns = [
        r'info@colorcraft\.com',
        r'admin@colorcraft\.com',
        r'info@colorandcraft\.com',
        r'admin@example\.com',
        r'test@example\.com'
    ]
    
    phone_patterns = [
        r'\+1 \(555\) 123-4567',
        r'\(555\) 123-4567',
        r'555-123-4567',
        r'\+15551234567'
    ]
    
    new_email = "Colour&craft@gmail.com"
    new_phone = "+44 7592 977155"
    
    # Files to update
    files_to_update = [
        'app/templates/contact.html',
        'app/templates/base.html',
        'app/templates/admin/login.html',
        'app/templates/admin/message_detail.html',
        'init_admin.py',
        'mysql_schema.sql',
        'config.py'
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            print(f"🔄 Updating {file_path}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update emails
            for pattern in email_patterns:
                content = re.sub(pattern, new_email, content, flags=re.IGNORECASE)
            
            # Update phone numbers
            for pattern in phone_patterns:
                content = re.sub(pattern, new_phone, content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Updated {file_path}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("\n🎉 Contact information update complete!")
    print(f"📧 All emails updated to: {new_email}")
    print(f"📞 All phones updated to: {new_phone}")

if __name__ == '__main__':
    update_contact_info()