from app.repositories.user_repo import UserRepository
from app.utils.custom_exceptions import UserNotFound
from app.policies.user_policy import UserPolicy

# These are different worklows, 
# I just put them in the same file for simplicity,
# yet I know they belong in separate files.
class GetUserProfileService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.policy = UserPolicy()
        
    def get(self, user_id, requester_id):
        user = self.repo.get_by_id(user_id)
        requester = self.repo.get_by_id(requester_id)
 
        if not user or not requester:
            raise UserNotFound()

        self.policy.can_view_profile(requester, user)
        
        return user

class GetAllUsersProfileService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.policy = UserPolicy()
        
    def get(self, requester_id):
        admin = self.repo.get_by_id(requester_id)
        if not admin:
            raise UserNotFound()

        self.policy.can_list_users(admin)
        
        users = self.repo.get_all_users()
        if not users:
            raise UserNotFound()
        
        return users