from app.repositories.token_repo import TokenRepository
from app.repositories.user_repo import UserRepository
from app.utils.custom_exceptions import UserNotFound
from flask_jwt_extended import create_access_token

class RefreshAccessTokenService:
    def __init__(self, token_repo: TokenRepository, user_repo: UserRepository):
        self.token_repo = token_repo
        self.user_repo = user_repo
                
    def refresh_access_token(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        
        if not user:
            raise UserNotFound()
        
        # New access token
        access_token = create_access_token(
            identity = str(user.id),
            additional_claims = {"role": user.role}
        )
        
        # Record JTI's for revocation
        self.token_repo.create_token_to_blacklist(access_token)
        return access_token