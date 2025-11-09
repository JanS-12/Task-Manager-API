from app.models.token_blocklist import TokenBlocklist
from flask_jwt_extended import decode_token
from datetime import datetime

def create_token_blocklist(token) -> TokenBlocklist:
    jti = decode_token(token)["jti"]
    user_id = decode_token(token)["sub"]
    type = decode_token(token)["type"]
    exp = datetime.fromtimestamp(decode_token(token)["exp"]) # SQLAlchemy DateTime, not seconds
    return TokenBlocklist(jti = jti, user_id = user_id, token_type = type, revoked_at = None, expires_at = exp)