from app.repositories.token_repo import TokenRepository 
from app.repositories.user_repo import UserRepository
from app.utils.custom_exceptions import UserNotFound

class LogoutService:
    def __init__(self, user_repo: UserRepository, token_repo: TokenRepository):
        self.token_repo = token_repo
        self.user_repo = user_repo
        
    def logout(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        
        self.token_repo.revoke_active_tokens(user.id)
        return
    