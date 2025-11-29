from sqlalchemy.sql import func
from app.extensions import db

class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"
    id          = db.Column(db.Integer, primary_key = True)
    jti         = db.Column(db.String(36), index = True, unique = True, nullable = False)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "CASCADE"), nullable = False, index = True)
    token_type  = db.Column(db.String(15), nullable = False)
    created_at  = db.Column(db.DateTime(timezone = True), server_default = func.now())
    revoked_at  = db.Column(db.DateTime(timezone = True), nullable = True)
    expires_at  = db.Column(db.DateTime(timezone = True), nullable = True)
    
    def is_revoked(self):
        return self.revoked_at is not None