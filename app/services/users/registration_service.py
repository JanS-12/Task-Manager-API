from app.utils.custom_exceptions import ExistingCredentialsError
from app.repositories.user_repo import UserRepository
from app.policies.user_policy import UserPolicy

class RegistrationService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.policy = UserPolicy()
        
    def create_profile(self, data):
        if self.repo.get_by_username(data["username"]):
            raise ExistingCredentialsError()

        return self.repo.create(data)