from werkzeug.security import generate_password_hash, check_password_hash

# Imagine this is what got stored in the database at registration time:
stored_hash = generate_password_hash("anothersecret")

print("stored_hash:", stored_hash)

print("correct password:", check_password_hash(stored_hash, "anothersecret"))
print("wrong password:", check_password_hash(stored_hash, "not-the-password"))
