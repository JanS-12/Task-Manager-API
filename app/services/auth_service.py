from flask_jwt_extended import create_access_token
from app.repositories.token_repo import TokenRepository
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema
from app.utils.logging import get_logger

auth_logger = get_logger("auth")
audit_logger = get_logger("audit")

class AuthService(): 
    def __init__(self, auth_repo: TokenRepository, user_service: UserService):
        self.auth_repo = auth_repo
        self.user_service = user_service
        self.user_schema = UserSchema()
        
    # Function to be called indirectly by the front-end client
    def refresh_access_token(self, requester_id):
        user = self.user_service.get_user(requester_id, requester_id)
        
        # New access token
        access_token = create_access_token(
            identity= str(user.id),
            additional_claims = {"role": user.role}
        )
        
        # Record JTI's for revocation
        self.auth_repo.create_token_to_blacklist(access_token)
        
        return {"access_token": access_token}
        
        
        
        
        
        
        