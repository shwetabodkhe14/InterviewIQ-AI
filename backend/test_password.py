from app.security.password import hash_password, verify_password

password = "MyPassword@123"

hashed = hash_password(password)

print("Original:", password)
print("Hash:", hashed)
print("Verification:", verify_password(password, hashed))