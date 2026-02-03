from app.repositories.project_repo import ProjectRepository
from app.repositories.user_repo import UserRepository
from app.policies.project_policy import ProjectPolicy
from app.utils.custom_exceptions import UserNotFound

class CreateProjectService:
    def __init__(self, project_repo: ProjectRepository, user_repo: UserRepository):
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.policy = ProjectPolicy()
        
    def create_project(self, data, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        
        project = self.project_repo.create_project(user_id, data)
        return project