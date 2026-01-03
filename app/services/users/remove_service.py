from app.repositories.user_repo import UserRepository
from app.repositories.token_repo import TokenRepository
from app.policies.user_policy import UserPolicy
from app.utils.custom_exceptions import UserNotFound

class RemoveUserService:
    def __init__(self, user_repo: UserRepository, token_repo: TokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.policy = UserPolicy()
        
    def remove(self, user_id, requester_id):
        requester = self.user_repo.get_by_id(requester_id)
        user = self.user_repo.get_by_id(user_id)
        
        if not user or not requester:
            raise UserNotFound()
        
        self.policy.can_delete_profile(requester)
        self.token_repo.revoke_active_tokens(user.id)
        self.user_repo.delete(user.id)