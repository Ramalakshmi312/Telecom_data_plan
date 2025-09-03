import bcrypt
import streamlit as st
from src.db import users_col

def hash_password(password: str) -> bytes:
    """Generate hashed password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    """Verify provided password against stored hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def register_user(email: str, password: str, name: str):
    """Register new user into MongoDB."""
    if users_col.find_one({"email": email}):
        return False, "User already exists."
    hashed_pw = hash_password(password)
    user_data = {
        "email": email,
        "password": hashed_pw,
        "name": name,
        "role": "Customer",  # default role
        "profile": {}        # empty profile to be filled later
    }
    users_col.insert_one(user_data)
    return True, "Registration successful."

def login_user(email: str, password: str):
    """Authenticate user, store user info in session state."""
    user = users_col.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        st.session_state['user'] = {
            "email": user['email'],
            "name": user['name'],
            "role": user.get('role', 'Customer')
        }
        return True
    return False
