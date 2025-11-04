from app.models.token_blocklist import TokenBlocklist
from flask_jwt_extended import decode_token

def create_token_blocklist(token) -> TokenBlocklist:
    jti = decode_token(token)["jti"]
    user_id = decode_token(token)["sub"]
    type = decode_token(token)["type"]
    return TokenBlocklist(jti = jti, user_id = user_id, token_type = type, revoked_at=None)