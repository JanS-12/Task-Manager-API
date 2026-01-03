from app.utils.custom_exceptions import NoDataError, InvalidCredentialsError
from flask_jwt_extended import create_access_token, create_refresh_token
from app.utils.security import check_password
from app.repositories.token_repo import TokenRepository
from app.repositories.user_repo import UserRepository

class LoginService:
    def __init__(self, token_repo: TokenRepository, user_repo: UserRepository):
        self.token_repo = token_repo
        self.user_repo = user_repo
        
    def login(self, username, password):
        user = self.user_repo.get_by_username(username)
        if not user or not check_password(password, user.password):
            raise InvalidCredentialsError()
        
        additional_claims = { "role": user.role }
        access_token = create_access_token(
            identity = str(user.id), 
            additional_claims = additional_claims
        )
        
        refresh_token = create_refresh_token(
            identity = str(user.id), 
            additional_claims = additional_claims
        )
        
        # Record JTI's for revocation       
        self.token_repo.create_token_to_blacklist(access_token)
        self.token_repo.create_token_to_blacklist(refresh_token)
        
        return {"access_token": access_token, "refresh_token": refresh_token}
            
        
        
        