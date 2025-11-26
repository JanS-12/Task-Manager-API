from app.models.token_blocklist import TokenBlocklist
from flask_jwt_extended import decode_token
from app.utils.logging import get_logger
from datetime import datetime
from app.extensions import db

auth_logger = get_logger("auth")

class TokenRepository():
    def create_token_to_blacklist(self, token):
        jti = decode_token(token)["jti"]
        user_id = decode_token(token)["sub"]
        type = decode_token(token)["type"]
        exp = datetime.fromtimestamp(decode_token(token)["exp"]) # SQLAlchemy DateTime, not seconds
        
        db.session.add(TokenBlocklist(jti=jti, user_id=user_id, token_type=type, expires_at=exp, revoked_at = None))
        db.session.commit()   
        
    def revoke_active_tokens(self, user_id):
        tokens = TokenBlocklist.query.filter_by(user_id = user_id, revoked_at=None).all()
        if tokens:
            for token in tokens:
                token.revoked_at = datetime.now()
                auth_logger.info(f"Token with jti \"{token.jti}\" has been revoked at \"{token.revoked_at}\".")
                
        db.session.commit()       
         
        