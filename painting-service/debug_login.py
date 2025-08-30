from werkzeug.security import generate_password_hash, check_password_hash

# Test the password hashing
test_username = "admin"
test_password = "admin123"

# Generate hash
password_hash = generate_password_hash(test_password)
print(f"Generated hash: {password_hash}")

# Test verification
is_valid = check_password_hash(password_hash, test_password)
print(f"Password verification: {is_valid}")

# Test with wrong password
wrong_password = "wrong123"
is_wrong = check_password_hash(password_hash, wrong_password)
print(f"Wrong password test: {is_wrong}")

print(f"\nExpected credentials:")
print(f"Username: {test_username}")
print(f"Password: {test_password}")