from passlib.hash import pbkdf2_sha256

# has a paswword
def hash_password(password):
    return pbkdf2_sha256.hash(password)

# for user authentication. It hashes the user-input password and compares that with the one we saved in the database.
def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)

