from werkzeug.security import generate_password_hash, check_password_hash

# Test the current password
test_password = "admin123"
hashed = generate_password_hash(test_password)
print(f"Password hash: {hashed}")
print(f"Password check: {check_password_hash(hashed, test_password)}")

# Test with your desired password
your_password = "your_new_password"  # Change this
your_hash = generate_password_hash(your_password)
print(f"Your password hash: {your_hash}")
print(f"Your password check: {check_password_hash(your_hash, your_password)}")