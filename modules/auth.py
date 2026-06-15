from modules.database import users
import bcrypt

def register_user(username, email, password):

    existing = users.find_one({
        "email": email
    })

    if existing:
        return False, "Email already exists"

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    users.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })

    return True, "Registration Successful"


def login_user(email, password):

    user = users.find_one({
        "email": email
    })

    if not user:
        return False, None

    if bcrypt.checkpw(
        password.encode(),
        user["password"]
    ):
        return True, user

    return False, None