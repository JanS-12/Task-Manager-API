from app.repositories.project_repo import ProjectRepository
from app.repositories.user_repo import UserRepository
from app.policies.project_policy import ProjectPolicy
from app.utils.custom_exceptions import UserNotFound, ProjectNotFound

class GetProjectService:
    def __init__(self, project_repo: ProjectRepository, user_repo: UserRepository):
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.policy = ProjectPolicy()
        
    def get_project(self, project_id, requester_id):
        requester = self.user_repo.get_by_id(requester_id)
        if not requester:
            raise UserNotFound()
        
        project = self.project_repo.get_a_project(project_id)
        if not project:
            raise ProjectNotFound()
        
        self.policy.can_view_project(requester, project)
        
        return project
        
        
        