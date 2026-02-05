from app.policies.project_policy import ProjectPolicy
from app.repositories.project_repo import ProjectRepository
from app.repositories.user_repo import UserRepository
from app.utils.custom_exceptions import UserNotFound, ProjectNotFound

class UpdateProjectService:
    def __init__(self, project_repo: ProjectRepository, user_repo: UserRepository):
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.policy = ProjectPolicy()
        
    def update_project(self, data, project_id, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        
        project = self.project_repo.get_a_project(project_id)
        if not project:
            raise ProjectNotFound()
        
        self.policy.can_update_project(user, project)
        project = self.project_repo.update_project(project.id, data)
        return project
       