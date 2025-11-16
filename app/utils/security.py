from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify
import bcrypt

def hash_password(plaintext: str) -> str:
    hashed = bcrypt.hashpw(plaintext.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")
    
def check_password(plaintext: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plaintext.encode("utf-8"), hashed_password.encode("utf-8"))

def role_required(allowed_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role not in allowed_roles:
                return jsonify(message = "Access Denied."), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper