from app.utils.custom_exceptions import NoDataError, InvalidCredentialsError, ExistingCredentialsError, UserNotFound
from flask_jwt_extended import (create_access_token, create_refresh_token)
from app.repositories.token_repo import TokenRepository
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema
from app.utils.security import check_password
from app.utils.logging import get_logger

auth_logger = get_logger("auth")
audit_logger = get_logger("audit")

class AuthService(): 
    def __init__(self, auth_repo: TokenRepository, user_service: UserService):
        self.auth_repo = auth_repo
        self.user_service = user_service
        self.user_schema = UserSchema()
          
    def register_user(self, data):
        if not data:
            raise NoDataError()
        
        # Validate and deserialize data
        user_data = self.user_schema.load(data)
        
        if self.user_service.get_user_by_username(user_data["username"]):
            raise ExistingCredentialsError()
        
        # Persist
        new_user = self.user_service.create_user(user_data)
        auth_logger.info(f"New user registered: \"{new_user.username}\" (\"{new_user.email}\")")
        return new_user
    
    def login(self, data):
        if not data:
            raise NoDataError()
        
         # Check if user exists
        user = self.user_service.get_user_by_username(data["username"])
        
        # Check Credentials
        if not user or not check_password(data["password"], user.password):
            auth_logger.info(f"Someone used the wrong credentials.")
            raise InvalidCredentialsError()
        
        # Create both Access and Refresh Tokens
        additional_claims = {"role": user.role}
        access_token = create_access_token(
            identity = str(user.id), 
            additional_claims = additional_claims
        )
        
        refresh_token = create_refresh_token(
            identity = str(user.id), 
            additional_claims = additional_claims
        )
        
        # Record JTI's for revocation       
        self.auth_repo.create_token_to_blacklist(access_token)
        self.auth_repo.create_token_to_blacklist(refresh_token)
        
        auth_logger.info(f"Access and refresh tokens created for \"{user.username}\".")
        audit_logger.info(f"User \"{user.username}\" has logged in.")
        return {"access_token": access_token, "refresh_token": refresh_token}
    
    def logout(self, user_id):
        user = self.user_service.get_user(user_id, user_id)
        if not user:
            raise UserNotFound()
        
        self.auth_repo.revoke_active_tokens(user_id)
        audit_logger.info(f"User \'{user.username}\' logged out.")
        
    # Function to be called indirectly by the front-end client
    def refresh_access_token(self, requester_id):
        user = self.user_service.get_user(requester_id, requester_id)
        if not user:
            raise UserNotFound()
        
        # New access token
        access_token = create_access_token(
            identity= str(user.id),
            additional_claims = {"role": user.role}
        )
        
        # Record JTI's for revocation
        self.auth_repo.create_token_to_blacklist(access_token)
        
        return {"access_token": access_token}
        
        
        
        
        
        
        