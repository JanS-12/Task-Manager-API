from app.utils.custom_exceptions import UserNotFound, AccessDenied
from app.repositories.user_repo import UserRepository

class UpdateUserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        
    def update(self, user_id, requester_id, data):
        user = self.repo.get_by_id(user_id)
        requester = self.repo.get_by_id(requester_id)
        
        if not user or not requester:
            raise UserNotFound()
        
        if requester.role != "admin" and requester.id != user.id:
            raise AccessDenied()

        user = self.repo.update(user.id, data)
        return user